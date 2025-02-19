'use client';
import React from 'react';
import Link from 'next/link';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { Heading, Paragraph } from '@/components/ui/typography';
import { Button } from '@/components/ui/button';
import { FileText, ArrowRight } from 'lucide-react';
import withAuth from '@/utils/withAuth';

interface Report {
  id: number;
  title: string;
  summary: string;
  date: string;
  category: string;
}

const reportsData: Report[] = [
  { 
    id: 1, 
    title: 'LLM Performance Analysis', 
    summary: 'A detailed analysis of LLM performance metrics including accuracy, F1 score, and response times.', 
    date: '2025-02-15', 
    category: 'Performance' 
  },
  { 
    id: 2, 
    title: 'Data Usage Report', 
    summary: 'Insights on data usage trends for the LLM including training data distribution and inference patterns.', 
    date: '2025-02-10', 
    category: 'Data' 
  },
  { 
    id: 3, 
    title: 'Training Time Analysis', 
    summary: 'Analysis of training time and resource usage across different model sizes and configurations.', 
    date: '2025-02-05', 
    category: 'Training' 
  },
  { 
    id: 4, 
    title: 'Inference Speed Analysis', 
    summary: 'Evaluation of inference speed across various models with benchmarks for different hardware setups.', 
    date: '2025-02-01', 
    category: 'Performance' 
  },
];

const ReportsPage: React.FC = () => {
  return (
    <div className="bg-background text-foreground p-4 sm:p-6 md:p-8 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12">
          <div className="flex items-center justify-center mb-4">
            <FileText className="h-8 w-8 text-primary mr-2" />
            <Heading size={1} className="text-center font-bold text-xl">Obsedian Reports</Heading>
          </div>
          {/* <Paragraph className="text-center text-lg text-muted-foreground max-w-2xl mx-auto">
            Browse our collection of reports that analyze the performance, data usage, and behavior patterns of our Language Models.
          </Paragraph> */}
        </header>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {reportsData.map((report) => (
            <Card 
              key={report.id} 
              className="flex flex-col h-full transition-all duration-300 hover:shadow-lg dark:hover:shadow-primary/10 hover:border-primary/50 group"
            >
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
                    {report.category}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    {new Date(report.date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </span>
                </div>
                <Heading size={3} className="mt-2 text-xl font-semibold group-hover:text-primary transition-colors">
                  {report.title}
                </Heading>
              </CardHeader>
              <CardContent className="flex-grow pb-2">
                <Paragraph className="text-muted-foreground">
                  {report.summary}
                </Paragraph>
              </CardContent>
              <CardFooter className="pt-4 pb-4">
                <Link href={`/reports/${report.id}`} className="w-full" passHref>
                  <Button 
                    variant="default" 
                    className="w-full group-hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
                  >
                    <span>View Report</span>
                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default withAuth(ReportsPage);