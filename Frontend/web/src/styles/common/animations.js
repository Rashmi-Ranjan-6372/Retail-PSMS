import { keyframes } from "@emotion/react";

export const floatBlob = keyframes`
  0% {transform: translate(0, 0);}
  50% {transform: translate(35px, 25px);}
  100% {transform: translate(0, 0);}
`;

export const floatIcon = keyframes`
  0% {transform: translateY(0) rotate(0deg) scale(1);}
  25% {transform: translateY(-18px) rotate(6deg) scale(1.04);}
  50% {transform: translateY(10px) rotate(-6deg) scale(.97);}
  75% {transform: translateY(-12px) rotate(4deg) scale(1.03);}
  100% {transform: translateY(0) rotate(0deg) scale(1);}
`;

export const fadeIn = keyframes`
  from {opacity: 0;}
  to {opacity: 1;}
`;

export const slideUp = keyframes`
  from {opacity: 0;transform: translateY(20px);}
  to {opacity: 1;transform: translateY(0);}
`;

export const scaleIn = keyframes`
  from {opacity: 0;transform: scale(.9);}
  to {opacity: 1;transform: scale(1);}
`;

export const spin = keyframes`
  from {transform: rotate(0deg);}
  to {transform: rotate(360deg);}
`;

export const pulse = keyframes`
  0% {transform: scale(1);}
  50% {transform: scale(1.05);}
  100% {transform: scale(1);}
`;

export const bounce = keyframes`
  0%, 100% {transform: translateY(0);}
  50% {transform: translateY(-8px);}
`;

export default {
    floatBlob,
    floatIcon,
    fadeIn,
    slideUp,
    scaleIn,
    spin,
    pulse,
    bounce
};