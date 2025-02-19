"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

// Define the form schema
const formSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().min(1, "Description is required"),
  devEnvUrl: z.string().url("Invalid URL").min(1, "Dev-Env URL is required"),
});

const AddDynamicLLMModelForm = () => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      description: "",
      devEnvUrl: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    const requestData = {
      title: data.title,
      description: data.description,
      devEnvUrl: data.devEnvUrl,
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
        console.log("Form submitted successfully");
        form.reset({
          title: "",
          description: "",
          devEnvUrl: "",
        });
      } else {
        const errorText = await response.text();
        console.error("Failed to submit form:", errorText);
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
            {/* Title Field */}
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter title" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Description Field */}
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter description" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Dev-Env URL Field */}
            <FormField
              control={form.control}
              name="devEnvUrl"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Dev-Env URL</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter Dev-Env URL" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Submit Button */}
            {/* <Button type="submit" className="w-96 self-center">Submit</Button> */}
          </form>
        </Form>
      </div>
    </main>
  );
};

export default AddDynamicLLMModelForm;