"use client";

import { useState } from "react";
import { X, Plus, Scan } from "lucide-react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import DynamicLLMModelAdd from "@/components/DynamicLLMModelAdd";
import StaticLLMModelAdd from "@/components/StaticLLMModelAdd";
import withAuth from '@/utils/withAuth';

const initialScanData = [
  {
    id: 1,
    title: "Web App - Example.com",
    status: "In Progress",
    org: "Org A",
    type: "dynamic",
  },
  {
    id: 2,
    title: "LLM - GPT-4 API",
    status: "In Queue",
    org: "Org B",
    type: "static",
  },
  {
    id: 3,
    title: "Mobile App - Demo App",
    status: "Completed",
    org: "Org C",
    type: "dynamic",
  },
  {
    id: 4,
    title: "Web App - Test.com",
    status: "Failed",
    org: "Org D",
    type: "static",
  },
];


function AnalysisPage() {
  const [scanData, setScanData] = useState(initialScanData);
  const [showScanTypeDialog, setShowScanTypeDialog] = useState(false);
  const [showScanFormDialog, setShowScanFormDialog] = useState(false);
  const [scanType, setScanType] = useState<"dynamic" | "static" | null>(null);
  const [formData, setFormData] = useState<any>(null);

  const handleAddScan = (type: "dynamic" | "static") => {
    setScanType(type);
    setShowScanTypeDialog(false);
    setShowScanFormDialog(true);
  };

  const handleFormSubmit = () => {
    if (!scanType || !formData) return;

    const newScan = {
      id: scanData.length + 1,
      title: formData.title || `${scanType === "dynamic" ? "Dynamic" : "Static"} Scan`,
      status: "In Queue",
      org: formData.org || "Org X",
      type: scanType,
    };

    setScanData([...scanData, newScan]);
    setShowScanFormDialog(false);
    setScanType(null);
    setFormData(null);
  };

  const handleViewAnalysis = (scanId: number) => {
    // ... (keep the same view analysis handler)
  };

  return (
    <div className="p-6 space-y-6 bg-background text-foreground">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Scan Queue</h1>
        <Button
          onClick={() => setShowScanTypeDialog(true)}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg rounded-full pl-6 pr-8 py-3 dark:from-blue-800 dark:to-purple-800 dark:hover:from-blue-900 dark:hover:to-purple-900"
        >
          <Plus className="mr-2 h-5 w-5" />
          Add New Scan
        </Button>
      </div>

      {/* Scan Type Selection Dialog */}
      <AlertDialog open={showScanTypeDialog} onOpenChange={setShowScanTypeDialog}>
        <AlertDialogContent className="rounded-xl max-w-md bg-card border border-border">
          <div className="relative">
            <button
              onClick={() => setShowScanTypeDialog(false)}
              className="absolute top-4 right-4 p-1 hover:bg-accent rounded-full text-foreground"
            >
              <X className="h-5 w-5" />
            </button>
            <AlertDialogHeader className="pt-8 px-6">
              <AlertDialogTitle className="text-xl text-center">
                Select Analysis Type
              </AlertDialogTitle>
              <AlertDialogDescription className="text-center text-muted-foreground">
                Choose the type of security analysis you want to perform
              </AlertDialogDescription>
            </AlertDialogHeader>
            
            <div className="p-6 space-y-4">
              <Button
                onClick={() => handleAddScan("dynamic")}
                className="w-full h-24 bg-blue-50 hover:bg-blue-100 border-2 border-blue-200 rounded-xl flex-col dark:bg-blue-900/20 dark:border-blue-800/50 dark:hover:bg-blue-900/30"
              >
                <Scan className="h-6 w-6 text-blue-600 mb-2 dark:text-blue-400" />
                <span className="text-blue-800 font-semibold dark:text-blue-200">Dynamic Analysis</span>
                <p className="text-sm text-blue-600 font-normal mt-1 dark:text-blue-300">
                  Real-time vulnerability scanning
                </p>
              </Button>

              <Button
                onClick={() => handleAddScan("static")}
                className="w-full h-24 bg-purple-50 hover:bg-purple-100 border-2 border-purple-200 rounded-xl flex-col dark:bg-purple-900/20 dark:border-purple-800/50 dark:hover:bg-purple-900/30"
              >
                <Scan className="h-6 w-6 text-purple-600 mb-2 dark:text-purple-400" />
                <span className="text-purple-800 font-semibold dark:text-purple-200">Static Analysis</span>
                <p className="text-sm text-purple-600 font-normal mt-1 dark:text-purple-300">
                  Code-level security inspection
                </p>
              </Button>
            </div>
          </div>
        </AlertDialogContent>
      </AlertDialog>

      {/* Scan Form Dialog */}
      <AlertDialog open={showScanFormDialog} onOpenChange={setShowScanFormDialog}>
        <AlertDialogContent className="rounded-xl max-w-2xl bg-card border border-border">
          <div className="relative">
            <button
              onClick={() => setShowScanFormDialog(false)}
              className="absolute top-4 right-4 p-1 hover:bg-accent rounded-full text-foreground"
            >
              <X className="h-5 w-5" />
            </button>
            <AlertDialogHeader className="pt-8 px-6">
              <AlertDialogTitle className="text-xl">
                {scanType === "dynamic" ? "Dynamic Analysis Setup" : "Static Analysis Configuration"}
              </AlertDialogTitle>
              <AlertDialogDescription className="text-muted-foreground">
                {scanType === "dynamic" 
                  ? "Configure parameters for dynamic vulnerability scanning"
                  : "Set up static code analysis parameters and rules"}
              </AlertDialogDescription>
            </AlertDialogHeader>

            <div className="p-6 space-y-6">
              {scanType === "dynamic" ? (
                <DynamicLLMModelAdd />
              ) : (
                <StaticLLMModelAdd />
              )}
            </div>

            <AlertDialogFooter className="px-6 pb-6">
              <Button 
                variant="outline" 
                onClick={() => setShowScanFormDialog(false)}
                className="px-8"
              >
                Cancel
              </Button>
              <Button 
                onClick={handleFormSubmit}
                className="bg-blue-600 hover:bg-blue-700 px-8 dark:bg-blue-800 dark:hover:bg-blue-900"
              >
                Start Analysis
              </Button>
            </AlertDialogFooter>
          </div>
        </AlertDialogContent>
      </AlertDialog>

      {/* Scan Table */}
      <Table className="border rounded-lg border-border">
        <TableCaption className="py-4 text-muted-foreground">Active and completed security scans</TableCaption>
        <TableHeader className="bg-accent">
          <TableRow>
            <TableHead className="font-semibold">Scan Title</TableHead>
            <TableHead className="font-semibold">Status</TableHead>
            <TableHead className="font-semibold">Organization</TableHead>
            <TableHead className="font-semibold text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {scanData.map((scan) => (
            <TableRow key={scan.id} className="hover:bg-accent/50">
              <TableCell className="font-medium">{scan.title}</TableCell>
              <TableCell>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm 
                  ${scan.status === "In Progress" ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-800/20 dark:text-yellow-200" :
                    scan.status === "In Queue" ? "bg-blue-100 text-blue-800 dark:bg-blue-800/20 dark:text-blue-200" :
                    scan.status === "Completed" ? "bg-green-100 text-green-800 dark:bg-green-800/20 dark:text-green-200" :
                    "bg-red-100 text-red-800 dark:bg-red-800/20 dark:text-red-200"}`}>
                  {scan.status}
                </span>
              </TableCell>
              <TableCell>{scan.org}</TableCell>
              <TableCell className="text-right">
                {scan.status === "Completed" && (
                  <Button
                    onClick={() => handleViewAnalysis(scan.id)}
                    variant="ghost"
                    className="text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/20"
                  >
                    View Report
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
export default withAuth(AnalysisPage);