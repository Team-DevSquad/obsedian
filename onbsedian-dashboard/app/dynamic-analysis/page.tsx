"use client";

import { useEffect, useRef, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Terminal, AlertCircle, Shield, Clock, RefreshCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { info } from "console";
import withAuth from '@/utils/withAuth';

const dummyData = [
  
  {
    "url": "https://kjsids.somaiya.edu/en",
    "issue": "Missing Security Headers: Cross-Origin-Embedder-Policy",
    "severity": "info",
    "description": "The Cross-Origin-Embedder-Policy header is missing, which controls cross-origin embedding.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/en",
    "issue": "Missing Security Headers: Cross-Origin-Opener-Policy",
    "severity": "info",
    "description": "The Cross-Origin-Opener-Policy header is missing, which controls cross-origin window interactions.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/en",
    "issue": "Missing Security Headers: Cross-Origin-Resource-Policy",
    "severity": "info",
    "description": "The Cross-Origin-Resource-Policy header is missing, which controls cross-origin resource sharing.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/",
    "issue": "Missing Security Headers: X-Frame-Options",
    "severity": "info",
    "description": "The X-Frame-Options header is missing, which prevents clickjacking attacks.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/",
    "issue": "Technology Detected: PHP",
    "severity": "info",
    "description": "The website is using PHP technology.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/client_secrets.json",
    "issue": "Gmail API Client Secrets Exposed",
    "severity": "info",
    "description": "The client_secrets.json file for Gmail API is exposed, which may contain sensitive credentials.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/vendor/composer/installed.json",
    "issue": "Composer Configuration Exposed",
    "severity": "info",
    "description": "The composer.json file is exposed, which may reveal installed dependencies and versions.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu//phpinfo.php",
    "issue": "PHPInfo File Exposed",
    "severity": "low",
    "description": "The phpinfo.php file is exposed, which may reveal sensitive server configuration details.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/desktop.ini",
    "issue": "Desktop.ini File Exposed",
    "severity": "info",
    "description": "The desktop.ini file is exposed, which may reveal directory configuration details.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/phpunit.xml",
    "issue": "PHPUnit Configuration Exposed",
    "severity": "info",
    "description": "The phpunit.xml file is exposed, which may reveal testing configuration details.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/robots.txt",
    "issue": "Robots.txt File Exposed",
    "severity": "info",
    "description": "The robots.txt file is exposed, which may reveal directory structure or sensitive paths.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/",
    "issue": "WAF Detected: Apache Generic",
    "severity": "info",
    "description": "A generic Apache WAF (Web Application Firewall) is detected.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/guest_auth/guestIsUp.php",
    "issue": "Ruijie EWEB Remote Code Execution (RCE)",
    "severity": "high",
    "description": "A remote code execution vulnerability in Ruijie EWEB was detected, which could allow an attacker to execute arbitrary code on the server.",
    "timestamp": "2024-02-18T10:30:00"
  },
  {
    "url": "https://kjsids.somaiya.edu/rest/api/user/picker?query=admin",
    "issue": "Jira Unauthenticated User Picker Vulnerability",
    "severity": "medium",
    "description": "An unauthenticated user picker vulnerability in Jira was detected, which could allow an attacker to enumerate users.",
    "timestamp": "2024-02-18T10:30:00"
  }
];


function DynamicAnalysisPage() {
  const terminalRef = useRef<HTMLDivElement>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [filter, setFilter] = useState("all");

  const getSeverityColor = (severity: string) => {
    const colors = {
      critical: "bg-red-500/10 text-red-500 border-red-500/20",
      high: "bg-orange-500/10 text-orange-500 border-orange-500/20",
      medium: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
      low: "bg-green-500/10 text-green-500 border-green-500/20",
      info: "bg-blue-500/10 text-blue-500 border-blue-500/20"
    };
    return colors[severity as keyof typeof colors] || "bg-blue-500/10 text-blue-500 border-blue-500/20";
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const filteredData = dummyData.filter(item => 
    filter === "all" || item.severity === filter
  );

  const startScan = () => {
    setIsScanning(true);
    // Simulate scan for 3 seconds
    setTimeout(() => setIsScanning(false), 3000);
  };

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [filteredData]);

  return (
    <div className="space-y-6">
      <Card className="border-none shadow-none bg-transparent">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-primary/10">
                <Terminal className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle>Dynamic Analysis</CardTitle>
                <CardDescription>Real-time vulnerability scanning results</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm text-muted-foreground">
                  Last scan: {formatTimestamp(dummyData[0].timestamp)}
                </span>
              </div>
              <Button 
                onClick={startScan} 
                disabled={isScanning}
                className="gap-2"
              >
                <RefreshCcw className={`h-4 w-4 ${isScanning ? 'animate-spin' : ''}`} />
                {isScanning ? 'Scanning...' : 'Start Scan'}
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="flex gap-2 mb-4">
        <Button
          variant={filter === "all" ? "default" : "outline"}
          onClick={() => setFilter("all")}
          className="gap-2"
        >
          <Shield className="h-4 w-4" />
          All
        </Button>
        <Button
          variant={filter === "critical" ? "default" : "outline"}
          onClick={() => setFilter("critical")}
          className="gap-2"
        >
          <AlertCircle className="h-4 w-4 text-red-500" />
          Critical
        </Button>
        <Button
          variant={filter === "high" ? "default" : "outline"}
          onClick={() => setFilter("high")}
          className="gap-2"
        >
          <AlertCircle className="h-4 w-4 text-orange-500" />
          High
        </Button>
        <Button
          variant={filter === "medium" ? "default" : "outline"}
          onClick={() => setFilter("medium")}
          className="gap-2"
        >
          <AlertCircle className="h-4 w-4 text-yellow-500" />
          Medium
        </Button>
        {/* info */}
        <Button
          variant={filter === "info" ? "default" : "outline"}
          onClick={() => setFilter("info")}
          className="gap-2"
        >
          <AlertCircle className="h-4 w-4 text-blue-500" />
          Info
        </Button>

        <Button
          variant={filter === "low" ? "default" : "outline"}
          onClick={() => setFilter("low")}
          className="gap-2"
        >
          <AlertCircle className="h-4 w-4 text-green-500" />
          Low
        </Button>
      </div>

      <Card>
        <CardContent className="p-0">
          <div
            ref={terminalRef}
            className="h-[600px] w-full overflow-y-auto rounded-lg divide-y divide-border"
          >
            {filteredData.map((item, index) => (
              <div key={index} className="p-4 hover:bg-muted/50 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className={getSeverityColor(item.severity)}>
                      {item.severity.toUpperCase()}
                    </Badge>
                    <span className="font-medium">{item.issue}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">
                    {formatTimestamp(item.timestamp)}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mb-2">{item.description}</p>
                <p className="text-sm font-mono text-muted-foreground">{item.url}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
export default withAuth(DynamicAnalysisPage);