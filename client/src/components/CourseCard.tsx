import React from 'react';
import { Box, Text, Stack, Badge, Heading } from '@chakra-ui/react';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import FusionCharts from "fusioncharts";
import ReactFusioncharts from "react-fusioncharts";
import Charts from "fusioncharts/fusioncharts.charts";

interface QuizData {
  accuracy: number;
  completeness: number;
  clarity: number;
  relevance: number;
  understanding: number;
  feedback: string;
}
Charts(FusionCharts);

interface CourseData {
  module_name: string;
  module_summary: string;
  quiz_score: [number | null, number | null, QuizData | null];
}

interface CardProps {
  courseData: CourseData;
}

const CourseCard: React.FC<CardProps> = ({ courseData }) => {
  const [quiz1Score, quiz2Score, quiz3Data] = courseData.quiz_score;

  const chartData = [['Quiz', 'Score'], ['Quiz 1', quiz1Score || 0], ['Quiz 2', quiz2Score || 0]];
  console.log(quiz3Data)

  const progressBarStyle = {
    textAlign: 'center',
    flex: 1,
    maxWidth: '150px',
  };

  const dataSource = {
    chart: {
      caption: "Countries with Highest Deforestation Rate",
      subcaption: "For the year 2023",
      yaxisname: "Deforested Area{br}(in Hectares)",
      decimals: "1",
      theme: "gammel",
    },
    data: [
      {
        label: "Completeness",
        value: quiz3Data.completeness
      },
      {
        label: "Accuracy",
        value: quiz3Data.accuracy
      },
      {
        label: "Clarity",
        value: quiz3Data.clarity
      },
      {
        label: "Relevance",
        value: quiz3Data.relevance
      },
      {
        label: "Understanding",
        value: quiz3Data.understanding
      },
    ]
  };

  return (
    <Box
      variant="outline"
      key={courseData.moduleTopic}
      mb={4}
      boxShadow="dark-lg"
      borderRadius="md"
      transition="transform 0.3s ease-in-out"
      _hover={{ transform: 'scale(1.03)' }}
    >
      <Stack p={4}>
        <Heading size="md">{courseData.module_name}</Heading>
        <Text py="2">{courseData.module_summary}</Text>
      </Stack>
      <Stack p={4} borderTopWidth="1px">
        {quiz3Data && (
          <Stack direction="row" spacing={4}>
            <Box style={progressBarStyle}>
              <CircularProgressbar
                value={(quiz3Data.accuracy || 0) * 10}
                text={`${quiz3Data.accuracy || 0}/10`}
                strokeWidth={10}
              />
              <Badge variant="solid" colorScheme="purple" fontSize={18} margin={3}>
                Accuracy
              </Badge>
            </Box>
            <Box style={progressBarStyle}>
              <CircularProgressbar
                value={(quiz3Data.completeness || 0) * 10}
                text={`${quiz3Data.completeness || 0}/10`}
                strokeWidth={10}
              />
              <Badge variant="solid" colorScheme="purple" fontSize={18} margin={3}>
                Completeness
              </Badge>
            </Box>
            <Box style={progressBarStyle}>
              <CircularProgressbar
                value={(quiz3Data.clarity || 0) * 10}
                text={`${quiz3Data.clarity || 0}/10`}
                strokeWidth={10}
              />
              <Badge variant="solid" colorScheme="purple" fontSize={18} margin={3}>
                Clarity
              </Badge>
            </Box>
            <Box style={progressBarStyle}>
              <CircularProgressbar
                value={(quiz3Data.relevance || 0) * 10}
                text={`${quiz3Data.relevance || 0}/10`}
                strokeWidth={10} />
              <Badge variant="solid" colorScheme="purple" fontSize={18} margin={3}>
                Relevance
              </Badge>
            </Box>
            <Box style={progressBarStyle}>
              <CircularProgressbar
                value={(quiz3Data.understanding || 0) * 10}
                text={`${quiz3Data.understanding || 0}/10`}
                strokeWidth={10}
              />
              <Badge variant="solid" colorScheme="purple" fontSize={18} margin={3}>
                Understanding
              </Badge>
            </Box>
          </Stack>
        )}
      </Stack>

      {quiz3Data && (
        <Box border="1px" borderColor="gray.300" p={4} borderRadius="md">
          <Badge variant="solid" colorScheme="purple" fontSize={18} margin={2}>
            Quiz Feedback
          </Badge>
          <Text className=" ">{quiz3Data.feedback}</Text>
        </Box>
      )}

      {/* <ReactFusioncharts
        type="column3d"
        width="50%"
        height="100%"
        dataFormat="JSON"
        dataSource={dataSource}
      /> */}
    </Box>
  );
};

export default CourseCard;