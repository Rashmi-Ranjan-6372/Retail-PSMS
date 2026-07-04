import { floatBlob, floatIcon } from "./animations";

export const pageContainer = {
  minH: "100vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  p: "20px",
  position: "relative",
  overflow: "hidden",
  fontFamily: "Inter, Arial, sans-serif",
  background: `
    linear-gradient(rgba(37,99,235,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37,99,235,.05) 1px, transparent 1px),
    linear-gradient(135deg,#F8FAFC 0%,#EEF6FF 45%,#E0F2FE 100%)
  `,
  backgroundSize: "60px 60px, 60px 60px, 100% 100%",
};

export const blobOne = {
  position: "absolute",
  width: "340px",
  height: "340px",
  borderRadius: "50%",
  filter: "blur(80px)",
  background: "rgba(37,99,235,.18)",
  top: "-120px",
  left: "-120px",
  zIndex: 0,
  animation: `${floatBlob} 12s ease-in-out infinite`,
};

export const blobTwo = {
  position: "absolute",
  width: "300px",
  height: "300px",
  borderRadius: "50%",
  filter: "blur(80px)",
  background: "rgba(14,165,233,.18)",
  bottom: "-120px",
  right: "-120px",
  zIndex: 0,
  animation: `${floatBlob} 12s ease-in-out infinite`,
  animationDelay: "4s",
};

export const pharmacyBackground = {
  position: "absolute",
  inset: 0,
  overflow: "hidden",
  pointerEvents: "none",
  zIndex: 1,
};

export const backgroundIcon = {
  position: "absolute",
  width: "80px",
  opacity: 0.07,
  filter:
    "invert(33%) sepia(91%) saturate(1050%) hue-rotate(200deg) brightness(105%)",
  animation: `${floatIcon} 20s ease-in-out infinite`,
  userSelect: "none",
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

export const center = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const rowBetween = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
};

export const columnCenter = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
};

export default {
    pageContainer,
    blobOne,
    blobTwo,
    pharmacyBackground,
    backgroundIcon,
    iconPositions,
    center,
    rowBetween,
    columnCenter,
};