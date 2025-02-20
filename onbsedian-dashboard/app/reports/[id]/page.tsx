'use client';
import React from 'react';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { Heading, Paragraph } from '@/components/ui/typography';
import { Button } from '@/components/ui/button';
import { FileText, ArrowLeft, Calendar, Briefcase, BarChart } from 'lucide-react';
import withAuth from '@/utils/withAuth';

const reportDetails: { 
  [key: string]: { 
    title: string; 
    content: string; 
    date: string;
    author: string;
    category: string;
    keyFindings: string[];
  } 
} = {
  '1': {
    title: 'LLM Performance Analysis',
    content: 'This report provides a comprehensive analysis of the performance metrics for our LLM models, including accuracy, F1 score, and other relevant KPIs. We observed significant improvements in performance when using larger context windows and more training data, though with diminishing returns beyond certain thresholds.',
    date: '2025-02-15',
    author: 'AI Research Team',
    category: 'Performance',
    keyFindings: [
      'Accuracy improved by 12% when doubling the context window',
      'Response latency increased by only 5% despite model size increase',
      'Fine-tuning on domain-specific data yielded 18% better results',
      'Resource utilization optimizations reduced inference costs by 22%'
    ]
  },
  '2': {
    title: 'Data Usage Report',
    content: 'This report provides detailed insights into the data usage trends observed during the training and inference phases of our LLM. We analyze how different data sources contribute to model performance and identify opportunities for optimization in our data pipeline.',
    date: '2025-02-10',
    author: 'Data Science Division',
    category: 'Data',
    keyFindings: [
      'Structured data led to 15% more consistent outputs',
      'Diverse training data reduced bias metrics by 30%',
      'Synthetic data augmentation improved rare case handling by 25%',
      'Continuous learning from user interactions improved relevance by 18%'
    ]
  },
  '3': {
    title: 'Training Time Analysis',
    content: 'This report details the training time required for different configurations of our LLM, along with resource utilization statistics. We explore the tradeoffs between model size, training time, and performance to identify optimal training strategies.',
    date: '2025-02-05',
    author: 'Infrastructure Team',
    category: 'Training',
    keyFindings: [
      'Distributed training reduced overall time by 60%',
      'GPU memory optimizations allowed 40% larger batch sizes',
      'Checkpoint strategies reduced recovery time by 75%',
      'Custom learning rate schedules converged 25% faster'
    ]
  },
  '4': {
    title: 'Inference Speed Analysis',
    content: 'This report evaluates the inference speed across various models and configurations, providing benchmarks for performance assessment. We analyze the impact of different optimization techniques like quantization, distillation, and hardware acceleration.',
    date: '2025-02-01',
    author: 'Performance Engineering Team',
    category: 'Performance',
    keyFindings: [
      'INT8 quantization improved throughput by 3.2x',
      'Model distillation maintained 95% accuracy while reducing size by 40%',
      'Tensor parallelism reduced latency by 45% for large requests',
      'Batching optimizations improved overall throughput by 60%'
    ]
  },
};

interface ReportDetailPageProps {
  params: {
    id: string;
  };
}

const ReportDetailPage: React.FC<ReportDetailPageProps> = ({ params }) => {
  const report = reportDetails[params.id];

  if (!report) {
    notFound();
  }

  return (
    <div className="bg-background text-foreground p-4 sm:p-6 md:p-8 min-h-screen">
      <div className="max-w-4xl mx-auto">
        <Card className="rounded-lg shadow-lg dark:shadow-primary/5 overflow-hidden border-primary/10">
          <CardHeader className="bg-primary/5 pb-4 relative">
            <Link href="/reports" passHref>
              <Button 
                variant="ghost" 
                size="sm" 
                className="absolute top-4 left-4 p-2 h-8 w-8"
                aria-label="Go back to reports"
              >
                <ArrowLeft className="h-4 w-4" />
              </Button>
            </Link>
            
            <div className="text-center pt-6">
              <div className="flex justify-center mb-4">
                <div className="inline-flex items-center justify-center p-2 bg-primary/10 rounded-full">
                  <FileText className="h-6 w-6 text-primary" />
                </div>
              </div>
              <Heading size={1} className="text-3xl font-bold mb-2">{report.title}</Heading>
              
              {/* Report metadata */}
              <div className="flex flex-wrap justify-center gap-4 mt-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1.5">
                  <Calendar className="h-4 w-4" />
                  <span>
                    {new Date(report.date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Briefcase className="h-4 w-4" />
                  <span>{report.author}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <BarChart className="h-4 w-4" />
                  <span>{report.category}</span>
                </div>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="px-6 py-8">
            {/* Main content */}
            <Paragraph className="text-lg leading-relaxed mb-8">
              {report.content}
            </Paragraph>
            
            {/* Key findings */}
            <div className="bg-primary/5 dark:bg-primary/10 rounded-lg p-6 mt-6">
              <Heading size={3} className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="inline-flex items-center justify-center p-1 bg-primary/20 rounded-full">
                  <BarChart className="h-4 w-4 text-primary" />
                </span>
                Key Findings
              </Heading>
              <ul className="space-y-2">
                {report.keyFindings.map((finding, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="inline-flex justify-center items-center h-5 w-5 text-xs font-medium rounded-full bg-primary text-primary-foreground mt-0.5">
                      {index + 1}
                    </span>
                    <Paragraph className="flex-1">{finding}</Paragraph>
                  </li>
                ))}
              </ul>
            </div>
          </CardContent>
          
          <CardFooter className="bg-muted/50 px-6 py-4 flex justify-between">
            <Link href="/reports" passHref>
              <Button variant="outline" className="flex items-center gap-2">
                <ArrowLeft className="h-4 w-4" />
                Back to Reports
              </Button>
            </Link>
            <Button variant="default">Download PDF</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default withAuth(ReportDetailPage);