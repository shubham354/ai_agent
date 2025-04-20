import React, { useState } from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  VStack,
  useToast,
  Button,
  SimpleGrid,
} from '@chakra-ui/react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface Visualization {
  type: string;
  title: string;
  data: any;
}

interface Analysis {
  analysis: any;
  visualizations: Visualization[];
  insights: string[];
}

const DataAnalysis: React.FC = () => {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setIsLoading(true);

    try {
      const response = await axios.post<Analysis>(
        'http://localhost:8000/analyze',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setAnalysis(response.data);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to analyze file',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const renderVisualization = (visualization: Visualization) => {
    const chartData = JSON.parse(visualization.data);

    switch (visualization.type) {
      case 'line':
        return <Line data={chartData} options={{ responsive: true }} />;
      case 'bar':
        return <Bar data={chartData} options={{ responsive: true }} />;
      case 'pie':
        return <Pie data={chartData} options={{ responsive: true }} />;
      default:
        return null;
    }
  };

  return (
    <Box p={4}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={4}>
            Data Analysis
          </Heading>
          <Button
            onClick={() => document.getElementById('analysis-file-upload')?.click()}
            isLoading={isLoading}
            colorScheme="blue"
          >
            Upload File
          </Button>
          <input
            id="analysis-file-upload"
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />
        </Box>

        {analysis && (
          <>
            <Box>
              <Heading size="md" mb={2}>
                Insights
              </Heading>
              <VStack align="stretch" spacing={2}>
                {analysis.insights.map((insight, index) => (
                  <Text key={index}>{insight}</Text>
                ))}
              </VStack>
            </Box>

            <Box>
              <Heading size="md" mb={4}>
                Visualizations
              </Heading>
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                {analysis.visualizations.map((viz, index) => (
                  <Box
                    key={index}
                    p={4}
                    borderWidth={1}
                    borderRadius="lg"
                    shadow="sm"
                  >
                    <Heading size="sm" mb={2}>
                      {viz.title}
                    </Heading>
                    {renderVisualization(viz)}
                  </Box>
                ))}
              </SimpleGrid>
            </Box>

            <Box>
              <Heading size="md" mb={2}>
                Basic Statistics
              </Heading>
              <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                <Box>
                  <Text fontWeight="bold">Total Rows:</Text>
                  <Text>{analysis.analysis.basic_info.rows}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold">Columns:</Text>
                  <Text>{analysis.analysis.basic_info.columns.join(', ')}</Text>
                </Box>
              </Grid>
            </Box>
          </>
        )}
      </VStack>
    </Box>
  );
};

export default DataAnalysis; 