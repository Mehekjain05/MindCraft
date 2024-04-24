import React, { useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  ButtonGroup,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  GridItem,
  Input,
  InputGroup,
  Progress,
  useColorModeValue,
  Radio,
  RadioGroup,
  Stack,
  useToast,
  Text,
  InputLeftElement,
  Select,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import Navbar_Landing from '../components/navbar';
import Footer from '../components/footer'
import { yupResolver } from "@hookform/resolvers/yup";
import { useNavigate } from 'react-router-dom';
import * as yup from "yup";



const form1Schema = yup.object().shape({
  firstName: yup.string().required("First name is required"),
  lastName: yup.string().required("Last name is required"),
  email: yup
    .string()
    .email("Please introduce a valid email")
    .required("Email is required"),
  password: yup
    .string()
    .min(8, "Password is too short - should be 8 chars minimum.")
    .matches(/[a-zA-Z]/, "Password can only contain Latin letters.")
    .required("Password is required"),
});

const form2Schema = yup.object().shape({
  country: yup.string().required("Country is required"),
  city: yup.string().required("City is required"),
  state: yup.string().required("State is required"),
  gender: yup.string().required("Gender is required"),
  age: yup.number().integer().min(1, 'Age must be a positive number').required('Age is required'),
  college: yup.string().required("College Name is required"),
  course: yup.string().required("Course Name is required"),
  interest: yup.string().required('Interest is required'),
});

const Form1 = ({ register, errors }: { register: any; errors: any }) => {
  return (
    <>
      <Text w="80vh" fontSize={'50px'} className='feature-heading' color={useColorModeValue('purple.600', 'purple.500')} textAlign={"center"} fontWeight="normal" mb="2%">
        <b>User Credentials</b>
      </Text>
      <Flex>
        <FormControl isInvalid={!!errors.firstName} mr="5%">
          <FormLabel htmlFor="first-name" fontWeight={"normal"}>
            First name
          </FormLabel>
          <Input id="first-name" name="first-name" placeholder="First name" {...register("firstName")} />
          <FormErrorMessage>
            {errors.firstName && errors.firstName.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.lastName}>
          <FormLabel htmlFor="last-name" fontWeight={"normal"}>
            Last name
          </FormLabel>
          <Input id="last-name" name="last-name" placeholder="Last name" {...register("lastName")} />
          <FormErrorMessage>
            {errors.lastName && errors.lastName.message}
          </FormErrorMessage>
        </FormControl>
      </Flex>
      <FormControl isInvalid={!!errors.email} mt="2%">
        <FormLabel htmlFor="email" fontWeight={"normal"}>
          Email address
        </FormLabel>
        <Input id="email" name="email" placeholder="Email address" type="email" {...register("email")} />
        <FormHelperText>We&apos;ll never share your email.</FormHelperText>
        <FormErrorMessage>
          {errors.email && errors.email.message}
        </FormErrorMessage>
      </FormControl>

      <FormControl isInvalid={!!errors.password}>
        <FormLabel htmlFor="password" fontWeight={"normal"} mt="2%">
          Password
        </FormLabel>
        <InputGroup size="md">
          <Input
            type="password"
            id="password"
            name="password"
            placeholder="Enter password"
            {...register("password")}
          />
        </InputGroup>
        <FormErrorMessage>
          {errors.password && errors.password.message}
        </FormErrorMessage>
      </FormControl>
    </>
  );
};

const Form2 = ({ register, errors, collegeIdFile, setCollegeIdFile }: { register: any; errors: any; collegeIdFile: File | null; setCollegeIdFile: React.Dispatch<React.SetStateAction<File | null>> }) => {

  return (
    <>
      <Text w="80vh" fontSize={'50px'} className='feature-heading' color={useColorModeValue('purple.600', 'purple.500')} textAlign={"center"} fontWeight="normal" mb="2%">
        User Details
      </Text>
      <Flex>
        <FormControl as={GridItem} colSpan={[6, 3]} isInvalid={!!errors.country} mb={4} mr="3%">
          <FormLabel
            htmlFor="country"
          >
            Country
          </FormLabel>
          <Input id="country" name="country" {...register("country")} />
          <FormErrorMessage>
            {errors.country && errors.country.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.state} mb={4}>
          <FormLabel htmlFor="state">State</FormLabel>
          <Input id="state" name="state" {...register("state")} />
          <FormErrorMessage>
            {errors.state && errors.state.message}
          </FormErrorMessage>
        </FormControl>
      </Flex>

      <FormControl isInvalid={!!errors.city} mb={4}>
        <FormLabel htmlFor="city">City</FormLabel>
        <Input id="city" name="city" {...register("city")} />
        <FormErrorMessage>
          {errors.city && errors.city.message}
        </FormErrorMessage>
      </FormControl>

      <Flex>
        <FormControl as={GridItem} colSpan={[6, 3]} isInvalid={!!errors.gender} mb={4} mr="3%">
          <FormLabel htmlFor="gender">Gender</FormLabel>
          <RadioGroup colorScheme='purple' id="gender" name="gender">
            <Stack direction="row">
              <Radio value="male" {...register('gender')}>Male</Radio>
              <Radio value="female" {...register('gender')}>Female</Radio>
              <Radio value="other" {...register('gender')}>Other</Radio>
            </Stack>
          </RadioGroup>
          <FormErrorMessage>
            {errors.gender && errors.gender.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.age} mb={4}>
          <FormLabel htmlFor="age">Age</FormLabel>
          <Input id="age" name="age" type="number" {...register('age')} />
          <FormErrorMessage>
            {errors.age && errors.age.message}
          </FormErrorMessage>
        </FormControl>
      </Flex>

      <Flex>
        <FormControl as={GridItem} colSpan={[6, 3]} isInvalid={!!errors.college} mb={4} mr="3%">
          <FormLabel htmlFor="college">
            College Name
          </FormLabel>
          <Input id="college" name="college" {...register("college")} />
          <FormErrorMessage>
            {errors.college && errors.college.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.course} mb={4}>
          <FormLabel htmlFor="course">Current Course</FormLabel>
          <Input id="course" name="course" {...register("course")} />
          <FormErrorMessage>
            {errors.course && errors.course.message}
          </FormErrorMessage>
        </FormControl>
      </Flex>


      {/* <FormControl isInvalid={!!errors.interest} mb={4}>
        <FormLabel htmlFor="interest">Interest</FormLabel>
        <Select
          id="interest"
          name="interest"
          variant="outline"
          colorScheme='purple'
          {...register('interest')} // Assuming you have updated the useForm hook to handle multiple selections
          multiple="true"
          placeholder="Select multiple interests"
        >
          <option value="Machine Learning">Machine Learning</option>
          <option value="Deep Learning">Deep Learning</option>
          <option value="Natural Language Processing">Natural Language Processing</option>
          <option value="Computer Vision">Computer Vision</option>
          <option value="Reinforcement Learning">Reinforcement Learning</option>
          <option value="Data Science">Data Science</option>
          <option value="Neural Networks">Neural Networks</option>
          <option value="AI Ethics">AI Ethics</option>
          <option value="TensorFlow">TensorFlow</option>
          <option value="PyTorch">PyTorch</option>
          <option value="Supervised Learning">Supervised Learning</option>
          <option value="Unsupervised Learning">Unsupervised Learning</option>
          <option value="Recommender Systems">Recommender Systems</option>
          <option value="Data Preprocessing">Data Preprocessing</option>
          <option value="Time Series Analysis">Time Series Analysis</option>
          <option value="Ensemble Learning">Ensemble Learning</option>
          <option value="Regression Analysis">Regression Analysis</option>
          <option value="Classification">Classification</option>
          <option value="Clustering">Clustering</option>
          <option value="Autoencoders">Autoencoders</option>
          <option value="Automobiles">Automobiles</option>
          <option value="Computer Vision">Computer Vision</option>
          <option value="Artificial Intelligence">Artificial Intelligence</option>
        </Select>
        <FormErrorMessage>
          {errors.interest && errors.interest.message}
        </FormErrorMessage>
      </FormControl> */}

      <FormControl isInvalid={!!errors.interest} mb={4}>
        <FormLabel htmlFor="interest">Interests</FormLabel>
        <Input
          id="interest"
          name="interest"
          variant="outline"
          colorScheme='purple'
          {...register('interest')}
          placeholder="List your interests using commas"
        />
        <FormErrorMessage>
          {errors.interest && errors.interest.message}
        </FormErrorMessage>
      </FormControl>

      <FormControl isInvalid={!!errors.collegeId} mb={4}>
        <FormLabel htmlFor="college-id">College ID</FormLabel>
        <InputGroup>
          <InputLeftElement pointerEvents='none' color='gray.300' fontSize='1.2em'>
          </InputLeftElement>
          <input
            id="college-id"
            name="college-id"
            type="file"
            accept="image/*" // Accept only images
            style={{ display: 'none' }}
            {...register('collegeId')}
            onChange={(e) => {
              setCollegeIdFile(e.target.files[0]);
            }}
          />
          <Button
            onClick={() => document.getElementById('college-id').click()}
            variant="outline"
            colorScheme="purple"
          >
            {collegeIdFile ? collegeIdFile.name : 'Upload College ID'}
          </Button>
        </InputGroup>
        <FormErrorMessage>
          {errors.collegeId && errors.collegeId.message}
        </FormErrorMessage>
      </FormControl>

    </>
  );
};

const Signup = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [progress, setProgress] = useState(50);
  const [collegeIdFile, setCollegeIdFile] = useState(null);

  const resolver: any = step === 1 ? yupResolver(form1Schema) : yupResolver(form2Schema);

  const {
    register,
    handleSubmit,
    formState: { errors },
    trigger,
  } = useForm({
    resolver: resolver,
  });

  const onSubmit = async (data: { [key: string]: any }) => {
    try {
      const formData = new FormData();
      formData.append('firstName', data.firstName);
      formData.append('lastName', data.lastName);
      formData.append('email', data.email);
      formData.append('password', data.password);

      // Append user details data
      formData.append('country', data.country);
      formData.append('state', data.state);
      formData.append('city', data.city);
      formData.append('gender', data.gender);
      formData.append('age', data.age);
      formData.append('college', data.college);
      formData.append('course', data.course);
      formData.append('interest', data.interest);

      // Append college ID file
      formData.append('collegeId', collegeIdFile);
      const response = await axios.post('/api/register', formData, {
        withCredentials: true, headers: {
          'Content-Type': 'multipart/form-data',
        }
      });

      if (response.data.response) {
        // Account created successfully
        toast({
          title: 'Account created.',
          description: "We've created your account for you. You can Login Now!!",
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
        console.log(response.data);
        navigate('/login');
      } else {
        // User already exists
        toast({
          title: 'Error',
          description: 'User already exists. Please use a different email address.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      // Display toast on general error
      toast({
        title: 'Error',
        description: 'An error occurred while creating the account.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      console.error(error);
    }
  };

  return (
    <div>
      <Navbar_Landing />
      <Flex
        minHeight='100vh' bg={useColorModeValue('purple.300', 'purple.800')} width='full' align='center' justifyContent='center'>
        <Box
          rounded="lg"
          my={10}
          bg={useColorModeValue('white', 'gray.900')}
          shadow="dark-lg"
          maxWidth={800}
          borderColor={useColorModeValue('purple.400', 'gray.900')}
          p={6}>
          <Progress colorScheme="purple" size="sm" value={progress} hasStripe mb="5%" mx="5%" isAnimated />
          <form onSubmit={handleSubmit(onSubmit)}>
            {step === 1 && <Form1 register={register} errors={errors} />}
            {step === 2 && <Form2 register={register} errors={errors} collegeIdFile={collegeIdFile} setCollegeIdFile={setCollegeIdFile} />}
            <ButtonGroup mt="5%" w="100%">
              <Flex w="100%" justifyContent="space-between">
                <Flex>
                  {step > 1 && (
                    <Button
                      variant="outline"
                      colorScheme="purple" _hover={{ bg: useColorModeValue('purple.600', 'purple.800'), color: useColorModeValue('white', 'white') }}
                      onClick={() => {
                        setStep(step - 1);
                        setProgress(progress - 50);
                      }}
                    >
                      Previous
                    </Button>
                  )}
                  {step < 2 && (
                    <Button
                      variant="outline"
                      colorScheme="purple" _hover={{ bg: useColorModeValue('purple.600', 'purple.800'), color: useColorModeValue('white', 'white') }}
                      onClick={async () => {
                        const isValid = await trigger();
                        if (isValid) {
                          setStep(step + 1);
                          setProgress(progress + 50);
                        }
                      }}
                    >
                      Next
                    </Button>
                  )}
                </Flex>
                {step === 2 && (
                  <Button
                    variant="outline"
                    colorScheme="purple" _hover={{ bg: useColorModeValue('purple.600', 'purple.800'), color: useColorModeValue('white', 'white') }}
                    type="submit">Submit</Button>
                )}
              </Flex>
            </ButtonGroup>
          </form>
        </Box>
      </Flex>

      <Footer />
    </div>
  );
}

export default Signup;
