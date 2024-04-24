import React, { useState } from 'react';
import { Image, Button } from "@chakra-ui/react";

const Slideshow = ({ images }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const goToNextImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex === images.length - 1 ? 0 : prevIndex + 1));
  };

  const goToPreviousImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? images.length - 1 : prevIndex - 1));
  };

  return (
    <div style={{ padding: "10px" }}>
      {images.map((image, index) => (
        <Image
          key={index}
          src={image}
          boxSize={{ base: '50px', md: '100px', lg: '500px' }}
          alt={`Slide ${index}`}
          style={{ display: index === currentIndex ? 'block' : 'none' }}
        />
      ))}
      <Button mt={2} onClick={goToPreviousImage} color={"white"}
        rounded="md"
        _hover={{
          transform: "translateY(-2px)",
          boxShadow: "md",
          transition: "transform 0.3s ease",  // Add transition property for smooth transition
          bg: "purple.600"
        }}
        bg={"purple.400"}>Previous</Button>
      <Button mt={2} style={{ "float": "right" }} color={"white"}
        rounded="md"
        _hover={{
          transform: "translateY(-2px)",
          boxShadow: "md",
          transition: "transform 0.3s ease",  // Add transition property for smooth transition
          bg: "purple.600"
        }}
        bg={"purple.400"} onClick={goToNextImage}>Next</Button>
    </div>
  );
};

export default Slideshow;
