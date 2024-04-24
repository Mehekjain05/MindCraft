import React, { useRef } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

interface ModelProps {
 position: [number, number, number];
 scale: number;
 isTalking: boolean;
}

export const Model: React.FC<ModelProps> = ({ position, scale, isTalking }) => {
 const group = useRef<THREE.Group>();
 const { nodes, materials } = useGLTF('/cartoon_teacher_model.glb');

 // Define initial scale
 const initialScale = new THREE.Vector3(40, 40, 40);
 const scaleRange = 0.3; // Range of scale variation
 const scaleSpeed = 4; // Speed of scale change

 useFrame((state, delta) => {
    if (group.current && isTalking) {
      // Calculate the new scale
      const currentScale = group.current.scale.clone();
      const direction = (Math.sin(state.clock.getElapsedTime() * scaleSpeed) + 1) / 2;
      const scaleFactor = 1 + direction * scaleRange;
      currentScale.set(scaleFactor, scaleFactor, scaleFactor);

      // Update the scale
      group.current.scale.copy(currentScale);
    }
 });

 // Render the model
 return (
    <group ref={group} position={position}>
      <primitive object={nodes.Sketchfab_Scene} dispose={null} scale={initialScale} position={[-9, -10, -15]} />
    </group>
 );
};
