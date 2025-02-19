'use client'
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
    productName: z.string().min(1, "Name is required"),
    repoType: z.enum(["github", "gitlab", "gitbucket"]),
    repoUrl: z.string().url("Invalid URL").min(1, "Repository URL is required"),
    accessToken: z.string().min(1, "Access token is required"),
    description: z.string().min(1, "Description is required"),
});

function AddStaticProductForm() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            productName: "",
            repoType: "github", // Default to GitHub
            repoUrl: "",
            accessToken: "",
            description: "",
        },
    });

    const onSubmit = async (data: z.infer<typeof formSchema>) => {
        const requestData = {
            name: data.productName,
            repoType: data.repoType,
            repoUrl: data.repoUrl,
            accessToken: data.accessToken,
            description: data.description,
        };

        console.log("Request Data:", JSON.stringify(requestData, null, 2));

        try {
            const response = await fetch('https://webhook.site/df997ad5-b9d7-43cc-97f9-0bd1df790a06/', {
                method: 'POST',
                mode: "no-cors",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NjU5OTMwLCJpYXQiOjE3Mjg1NzM1MzAsImp0aSI6ImJmZTUzZTE3ZjIwMzQ5YmI5YjlkM2VmM2JmZGFlMTQzIiwidXNlcl9pZCI6N30.joO-RIlt2QfeyNylJwcf0SIhFCQpTAcv02zBbeK3D1w',
                },
                body: JSON.stringify(requestData),
            });

            if (response.ok) {
                console.log("Product added successfully");
                form.reset({
                    productName: "",
                    repoType: "github",
                    repoUrl: "",
                    accessToken: "",
                    description: "",
                });
            } else {
                const errorText = await response.text();
                console.error("Failed to add product:", errorText);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <main className="w-full flex justify-center">
            <div className="w-full">
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2 flex flex-col">
                        <FormField
                            control={form.control}
                            name="productName"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Product Name</FormLabel>
                                    <FormControl>
                                        <Input placeholder="Product name" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="repoType"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Repository Type  </FormLabel>
                                    <FormControl>
                                        <select {...field} className="p-2 border rounded">
                                            <option value="github">GitHub</option>
                                            <option value="gitlab">GitLab</option>
                                            <option value="gitbucket">GitBucket</option>
                                        </select>
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="repoUrl"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Repository URL</FormLabel>
                                    <FormControl>
                                        <Input placeholder="https://github.com/username/repo" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="accessToken"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Access Token</FormLabel>
                                    <FormControl>
                                        <Input type="password" placeholder="Access token" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="description"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Description</FormLabel>
                                    <FormControl>
                                        <Input placeholder="A brief description of the product" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        {/* <Button type="submit" className="w-96 self-center">Add Product</Button> */}
                    </form>
                </Form>
            </div>
        </main>
    );
}

export default AddStaticProductForm;