"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { BugIcon, CodeSquare, ShieldAlert, Lightbulb, ChevronDown, ChevronUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import withAuth from '@/utils/withAuth';

// Dummy data for vulnerabilities
const vulnerabilities = [{
  "id": "A2:2023",
  "title": "Credentials Disclosure",
  "severity": "Critical",
  "description": "Sensitive credentials, such as access tokens, were exposed in the HTTP response. This could allow attackers to gain unauthorized access to protected resources.",
  "vulnerableCode": `const response = {
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
};`,
  "fix": `// Ensure sensitive credentials are not exposed in HTTP responses.
const response = {
  "message": "Authentication successful"
};`,
  "tips": "Avoid exposing sensitive credentials like access tokens in HTTP responses. Use secure storage mechanisms (e.g., HTTP-only cookies) and ensure proper access controls are in place."
},
{
  "id": "A07:2021-Identificatiion and Authenticatio Failures",
  "vulnerability_type": [
      "A07:2021-Identificatiion and Authenticatio Failures"
  ],
  "title": "Unsecured dependencies found in 'mongoose'",
  "severity": "medium",
  "location": {
      "filePath": "/tmp/Institute-Result-Management-System_5f22b1ff/server/package.json",
      "lineNumber": 17
  },
  "description": "The following dependency 'mongoose' (6.2.0) has been identified as having security vulnerabilities:  <https://npmjs.com/advisories/1938>",
  "fix": "Upgrade mongoose to a patched version or use a more secure alternative.",
  "tips": [
      "Review and apply all available patches for 'mongoose'.",
      "Consider using a more secure alternative to 'mongoose' such as MongoDB's official driver: <https://docs.mongodb.com/drivers/node/current/>"
  ]
},
{
  "id": "A01:2021-Broken Access Control",
  "vulnerability_type": [
      "A01:2021-Broken Access Control"
  ],
  "title": "Unrestricted access to 'jsonwebtoken'",
  "severity": "high",
  "location": {
      "filePath": "/tmp/Institute-Result-Management-System_5f22b1ff/server/package.json",
      "lineNumber": 19
  },
  "description": "The 'jsonwebtoken' package is vulnerable to unrestricted access, which may lead to unauthorized data manipulation or system compromise.",
  "fix": "Upgrade jsonwebtoken to a patched version (>=8.6.0).",
  "tips": [
      "Review and apply all available patches for 'jsonwebtoken'.",
      "Consider using a more secure alternative to 'jsonwebtoken' such as 'jose' or 'crypto-js'.",
      "Implement proper access controls and authentication mechanisms."
  ]
},
{
  "id": "A03:2021-Injection",
  "vulnerability_type": [
      "A03:2021-Injection"
  ],
  "title": "Insecure use of 'build' option in Docker Compose file may lead to command injection vulnerabilities",
  "severity": "High",
  "location": {
      "file_path": "/tmp/Institute-Result-Management-System_5f22b1ff/docker-compose.yaml",
      "line_number": 4
  },
  "description": "The 'build' option in the Docker Compose file specifies the context directory and Dockerfile to use for building the service images. If this value is not properly validated or sanitized, it may allow an attacker to inject malicious commands during the build process.",
  "fix": "Ensure that the provided context directory and Dockerfile paths are properly validated and sanitized to prevent command injection vulnerabilities. Consider using secure methods for building Docker images, such as multi-stage builds and restricting user privileges.",
  "tips": [
      "Consider using a Docker image from a trusted source or repository instead of relying on the 'build' option.",
      "Perform regular security audits and vulnerability assessments to identify and address any potential injection points in your Docker Compose files."
  ]
},


]

// Helper function to get severity color
const getSeverityColor = (severity: string) => {
  switch (severity) {
    case "Critical":
      return "text-red-500 dark:text-red-400";
    case "High":
      return "text-orange-500 dark:text-orange-400";
    case "Medium":
      return "text-yellow-500 dark:text-yellow-400";
    case "Low":
      return "text-blue-500 dark:text-blue-400";
    default:
      return "text-gray-500 dark:text-gray-400";
  }
};

// Helper function to get severity badge color
const getSeverityBadgeColor = (severity: string) => {
  switch (severity) {
    case "Critical":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
    case "High":
      return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200";
    case "Medium":
      return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
    case "Low":
      return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
    default:
      return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200";
  }
};
function StaticAnalysisPage() {
  const [expandedIds, setExpandedIds] = useState<string[]>([]);
  const [filter, setFilter] = useState("all");

  const toggleExpand = (id: string) => {
    setExpandedIds(prevIds =>
      prevIds.includes(id)
        ? prevIds.filter(prevId => prevId !== id)
        : [...prevIds, id]
    );
  };

  const filteredVulnerabilities = filter === "all"
    ? vulnerabilities
    : vulnerabilities.filter(v => v.severity.toLowerCase() === filter.toLowerCase());

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <ShieldAlert className="h-6 w-6 text-primary" />
          Static Analysis Results
        </h1>
        
        <div className="w-full md:w-auto">
          <Tabs defaultValue="all" value={filter} onValueChange={setFilter} className="w-full md:w-auto">
            <TabsList className="grid grid-cols-5 w-full">
              <TabsTrigger value="all">All</TabsTrigger>
              <TabsTrigger value="critical">Critical</TabsTrigger>
              <TabsTrigger value="high">High</TabsTrigger>
              <TabsTrigger value="medium">Medium</TabsTrigger>
              <TabsTrigger value="low">Low</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </div>

      <div className="space-y-6">
        {filteredVulnerabilities.length === 0 ? (
          <Card className="bg-background p-8">
            <CardContent className="flex flex-col items-center justify-center pt-6">
              <ShieldAlert className="h-12 w-12 text-green-500 mb-4" />
              <p className="text-xl font-medium text-center">No vulnerabilities found with this severity level</p>
            </CardContent>
          </Card>
        ) : (
          filteredVulnerabilities.map((vuln) => {
            const isExpanded = expandedIds.includes(vuln.id);
            
            return (
              <Card key={vuln.id} className="bg-background border border-border transition-all hover:shadow-md">
                <CardHeader className="cursor-pointer" onClick={() => toggleExpand(vuln.id)}>
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      <BugIcon className={`h-5 w-5 mt-1 ${getSeverityColor(vuln.severity.charAt(0).toUpperCase() + vuln.severity.slice(1))}`} />
                      <div>
                        <CardTitle className="text-lg">
                          {vuln.title}
                          <Badge variant="outline" className={`ml-2 text-xs py-0 ${getSeverityBadgeColor(vuln.severity.charAt(0).toUpperCase() + vuln.severity.slice(1))}`}>
                            {vuln.severity.charAt(0).toUpperCase() + vuln.severity.slice(1)}
                          </Badge>
                        </CardTitle>
                        <CardDescription className="mt-1 line-clamp-2 md:line-clamp-none">
                          {vuln.description}
                        </CardDescription>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-8 w-8 p-0 rounded-full"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleExpand(vuln.id);
                      }}
                    >
                      {isExpanded ? (
                        <ChevronUp className="h-4 w-4" />
                      ) : (
                        <ChevronDown className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </CardHeader>

                {isExpanded && (
                  <>
                    <CardContent>
                      <div className="space-y-6">
                        {/* Tabs for Code and Fix */}
                        <Tabs defaultValue="vulnerable" className="w-full">
                          <TabsList className="grid grid-cols-2">
                            <TabsTrigger value="vulnerable">Vulnerable Code</TabsTrigger>
                            <TabsTrigger value="fix">Fix</TabsTrigger>
                          </TabsList>
                          <TabsContent value="vulnerable" className="mt-2">
                            <div className="bg-muted rounded-lg overflow-hidden">
                              <pre className="p-4 text-sm font-mono overflow-x-auto">
                                <code>{vuln.vulnerableCode}</code>
                              </pre>
                            </div>
                          </TabsContent>
                          <TabsContent value="fix" className="mt-2">
                            <div className="bg-muted rounded-lg overflow-hidden">
                              <pre className="p-4 text-sm font-mono overflow-x-auto">
                                <code>{vuln.fix}</code>
                              </pre>
                            </div>
                          </TabsContent>
                        </Tabs>

                        {/* Best Practices */}
                        <div className="bg-primary/5 dark:bg-primary/10 p-4 rounded-lg flex items-start gap-3">
                          <Lightbulb className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                          <div>
                            <h3 className="font-semibold text-sm mb-1">Best Practices</h3>
                            <p className="text-sm text-muted-foreground">{vuln.tips}</p>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                    <CardFooter className="text-sm text-muted-foreground">
                      <p>Reference: {vuln.id}</p>
                    </CardFooter>
                  </>
                )}
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
}
export default withAuth(StaticAnalysisPage);