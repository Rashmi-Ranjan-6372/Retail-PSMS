import { floatBlob, floatIcon } from "./animations";
import { colors } from "./colors";

export const pageBackground = {
  position: "absolute",
  inset: 0,
  overflow: "hidden",
  pointerEvents: "none",
  zIndex: 1,
};

export const backgroundIcon = {
  position: "absolute",
  opacity: 0.07,
  filter:
    "invert(33%) sepia(91%) saturate(1050%) hue-rotate(200deg) brightness(105%)",
  animation: `${floatIcon} 20s ease-in-out infinite`,
};

export const iconPositions = {
  icon1: { top: "8%", left: "8%", width: "70px", animationDelay: "0s" },
  icon2: { top: "14%", right: "8%", width: "90px", animationDelay: "2s" },
  icon3: { top: "40%", left: "5%", width: "75px", animationDelay: "5s" },
  icon4: { top: "48%", right: "4%", width: "82px", animationDelay: "8s" },
  icon5: { bottom: "10%", left: "10%", width: "88px", animationDelay: "10s" },
  icon6: { bottom: "8%", right: "8%", width: "75px", animationDelay: "13s" },
  icon7: { bottom: "4%", left: "45%", width: "90px", animationDelay: "16s" },
  icon8: { top: "5%", left: "45%", width: "85px", animationDelay: "20s" },
  icon9: { top: "30%", left: "25%", width: "80px", animationDelay: "22s" },
  icon10: { top: "25%", right: "25%", width: "90px", animationDelay: "24s" },
  icon11: { bottom: "22%", left: "30%", width: "82px", animationDelay: "26s" },
  icon12: { bottom: "20%", right: "28%", width: "78px", animationDelay: "28s" },
};

export const blobOne = {
  position: "absolute",
  width: "340px",
  height: "340px",
  borderRadius: "50%",
  filter: "blur(80px)",
  background: `${colors.primary}30`, 
  top: "-120px",
  left: "-120px",
  animation: `${floatBlob} 12s ease-in-out infinite`,
};

export const blobTwo = {
  position: "absolute",
  width: "300px",
  height: "300px",
  borderRadius: "50%",
  filter: "blur(80px)",
  background: `${colors.secondary}30`, 
  bottom: "-120px",
  right: "-120px",
  animation: `${floatBlob} 12s ease-in-out infinite`,
  animationDelay: "4s",
};

export default {
  pageBackground,
  backgroundIcon,
  iconPositions,
  blobOne,
  blobTwo,
};
