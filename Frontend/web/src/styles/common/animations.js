// src/styles/common/animations.js

import { keyframes } from "@emotion/react";

export const floatBlob = keyframes`
  0% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(35px, 25px);
  }

  100% {
    transform: translate(0, 0);
  }
`;

export const floatIcon = keyframes`
  0% {
    transform: translateY(0) rotate(0deg) scale(1);
  }

  25% {
    transform: translateY(-18px) rotate(6deg) scale(1.04);
  }

  50% {
    transform: translateY(10px) rotate(-6deg) scale(.97);
  }

  75% {
    transform: translateY(-12px) rotate(4deg) scale(1.03);
  }

  100% {
    transform: translateY(0) rotate(0deg) scale(1);
  }
`;

export const fadeIn = keyframes`
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
`;

export const slideUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

export const slideDown = keyframes`
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

export const slideLeft = keyframes`
  from {
    opacity: 0;
    transform: translateX(20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
`;

export const slideRight = keyframes`
  from {
    opacity: 0;
    transform: translateX(-20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
`;

export const scaleIn = keyframes`
  from {
    opacity: 0;
    transform: scale(.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
`;

export const spin = keyframes`
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
`;

export const pulse = keyframes`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }

  100% {
    transform: scale(1);
  }
`;

export const bounce = keyframes`
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-8px);
  }
`;

export const shake = keyframes`
  0%,
  100% {
    transform: translateX(0);
  }

  20% {
    transform: translateX(-6px);
  }

  40% {
    transform: translateX(6px);
  }

  60% {
    transform: translateX(-4px);
  }

  80% {
    transform: translateX(4px);
  }
`;

export const logoFloat = keyframes`
  0% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }

  100% {
    transform: translateY(0);
  }
`;

export default {
  floatBlob,
  floatIcon,
  fadeIn,
  slideUp,
  slideDown,
  slideLeft,
  slideRight,
  scaleIn,
  spin,
  pulse,
  bounce,
  shake,
  logoFloat,
};