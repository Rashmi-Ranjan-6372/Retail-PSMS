import { floatBlob, floatIcon } from "./animations";
import { colors } from "./colors";

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

export const row = {
  display: "flex",
  alignItems: "center",
};

export const column = {
  display: "flex",
  flexDirection: "column",
};

export const rowCenter = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const rowBetween = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
};

export const rowAround = {
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
};

export const rowEvenly = {
  display: "flex",
  justifyContent: "space-evenly",
  alignItems: "center",
};

export const columnCenter = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
};

export const contentContainer = {
  width: "100%",
  maxW: "1280px",
  mx: "auto",
  px: "24px",
};

export const fluidContainer = {
  width: "100%",
  px: "24px",
};

export const sectionContainer = {
  py: "24px",
};

export const pageContent = {
  flex: 1,
  overflowY: "auto",
  p: "24px",
};

export const gridTwo = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
  },
  gap: "24px",
};

export const gridThree = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
    lg: "repeat(3,1fr)",
  },
  gap: "24px",
};

export const gridFour = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
    xl: "repeat(4,1fr)",
  },
  gap: "24px",
};

export const sidebarContainer = {
  display: "flex",
  flexDirection: "column",
  minH: "100vh",
  w: "260px",
  bg: colors.white,
  borderRight: `1px solid ${colors.borderLight}`,
  boxShadow: `0 2px 10px ${colors.shadow}`,
};

export const sidebarHeader = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  py: "20px",
  borderBottom: `1px solid ${colors.borderLight}`,
};

export const sidebarContent = {
  flex: 1,
  overflowY: "auto",
  py: "10px",
};

export const pageHeader = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  mb: "24px",
};

export const stickyHeader = {
  position: "sticky",
  top: 0,
  zIndex: 100,
  bg: colors.white,
  borderBottom: `1px solid ${colors.borderLight}`,
  px: "24px",
  py: "16px",
};

export const scrollContainer = {
  overflowY: "auto",
};

export const fullHeight = {
  minH: "100vh",
};

export const fullWidth = {
  width: "100%",
};

export const linkContainer = {
  display: "flex",
  justifyContent: "flex-end",
  alignItems: "center",
  mt: "-8px",
  mb: "20px",
};

export const flexCenter = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};

export const flexBetween = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
};

export const flexGap = {
  display: "flex",
  alignItems: "center",
  gap: "10px",
};

export const textCenter = {
  textAlign: "center",
};

export const pageWrapper = {
  minH: "100vh",
  bg: colors.background,
};

export const cardContainer = {
  width: "100%",
  maxW: "1200px",
  mx: "auto",
};

export const flexColumn = {
  display: "flex",
  flexDirection: "column",
};

export const flexWrap = {
  display: "flex",
  flexWrap: "wrap",
};

export const flexStart = {
  display: "flex",
  justifyContent: "flex-start",
  alignItems: "center",
};

export const flexEnd = {
  display: "flex",
  justifyContent: "flex-end",
  alignItems: "center",
};

export const flexAround = {
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
};

export const flexEvenly = {
  display: "flex",
  justifyContent: "space-evenly",
  alignItems: "center",
};

export const stack = {
  display: "flex",
  flexDirection: "column",
  gap: "16px",
};

export const horizontalStack = {
  display: "flex",
  alignItems: "center",
  gap: "16px",
};

export const sectionGap = {
  display: "flex",
  flexDirection: "column",
  gap: "24px",
};

export const dividerSpace = {
  my: "24px",
};

export const responsiveContainer = {
  width: "100%",
  maxW: {
    base: "100%",
    md: "720px",
    lg: "960px",
    xl: "1280px",
  },
  mx: "auto",
  px: "24px",
};

export const responsiveGrid = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
    lg: "repeat(3,1fr)",
    xl: "repeat(4,1fr)",
  },
  gap: "24px",
};

export const dashboardLayout = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    lg: "260px 1fr",
  },
  minH: "100vh",
};

export const centeredContent = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minH: "100vh",
};

export const stickyFooter = {
  mt: "auto",
};

export const overflowHidden = {
  overflow: "hidden",
};

export const overflowAuto = {
  overflow: "auto",
};

export const relative = {
  position: "relative",
};

export const absoluteFill = {
  position: "absolute",
  inset: 0,
};

/* ===========================================
   COMMON WRAPPERS
=========================================== */

export const appContainer = {
  width: "100%",
  minH: "100vh",
  bg: colors.background,
};

export const contentWrapper = {
  width: "100%",
  maxW: "1440px",
  mx: "auto",
  px: {
    base: "16px",
    md: "24px",
    lg: "32px",
  },
};

export const section = {
  py: "24px",
};

export const cardGrid = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
    lg: "repeat(3,1fr)",
  },
  gap: "20px",
};

export const formContainer = {
  display: "flex",
  flexDirection: "column",
  gap: "18px",
};

export const formRow = {
  display: "grid",
  gridTemplateColumns: {
    base: "1fr",
    md: "repeat(2,1fr)",
  },
  gap: "20px",
};

export const actionContainer = {
  display: "flex",
  justifyContent: "flex-end",
  alignItems: "center",
  gap: "12px",
  mt: "24px",
};

export const pageSection = {
  display: "flex",
  flexDirection: "column",
  gap: "24px",
};

export const tableWrapper = {
  overflowX: "auto",
  borderRadius: "12px",
};

export const emptyState = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  py: "60px",
  gap: "12px",
};

export const modalContent = {
  display: "flex",
  flexDirection: "column",
  gap: "20px",
};

export const drawerContent = {
  display: "flex",
  flexDirection: "column",
  gap: "18px",
};

export const stickyTop = {
  position: "sticky",
  top: 0,
  zIndex: 100,
};

export const stickyBottom = {
  position: "sticky",
  bottom: 0,
  zIndex: 100,
};

export const scrollY = {
  overflowY: "auto",
};

export const scrollX = {
  overflowX: "auto",
};

export const fullScreenCenter = {
  minH: "100vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const fullScreenColumn = {
  minH: "100vh",
  display: "flex",
  flexDirection: "column",
};

export const grow = {
  flex: 1,
};

export const shrink = {
  flexShrink: 0,
};

export const relativeContainer = {
  position: "relative",
};

export const absoluteCenter = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
};

export const absoluteTopRight = {
  position: "absolute",
  top: "16px",
  right: "16px",
};

export const absoluteTopLeft = {
  position: "absolute",
  top: "16px",
  left: "16px",
};

export const absoluteBottomRight = {
  position: "absolute",
  bottom: "16px",
  right: "16px",
};

export const absoluteBottomLeft = {
  position: "absolute",
  bottom: "16px",
  left: "16px",
};

export const sidebarItem = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  py: "13px",
  pr: "14px",
  cursor: "pointer",
  transition: "all .25s ease",
};

export const sidebarItemContent = {
  display: "flex",
  alignItems: "center",
  gap: "12px",
};

export const sidebarSubMenu = {
  mt: "4px",
};

export const sidebarLogoContainer = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export const sidebarLogo = {
  w: "120px",
  h: "auto",
  objectFit: "contain",
};

export const sidebarChevron = {
  fontSize: "12px",
  transition: ".25s",
};

export default {
  pageContainer,
  blobOne,
  blobTwo,
  pharmacyBackground,
  backgroundIcon,
  iconPositions,
  center,
  row,
  column,
  rowCenter,
  rowBetween,
  rowAround,
  rowEvenly,
  columnCenter,
  contentContainer,
  fluidContainer,
  sectionContainer,
  pageContent,
  gridTwo,
  gridThree,
  gridFour,
  sidebarContainer,
  sidebarHeader,
  sidebarContent,
  pageHeader,
  stickyHeader,
  scrollContainer,
  fullHeight,
  fullWidth,
  linkContainer,
  flexCenter,
  flexBetween,
  flexGap,
  textCenter,
  pageWrapper,
  cardContainer,
  flexColumn,
  flexWrap,
  flexStart,
  flexEnd,
  flexAround,
  flexEvenly,
  stack,
  horizontalStack,
  sectionGap,
  dividerSpace,
  responsiveContainer,
  responsiveGrid,
  dashboardLayout,
  centeredContent,
  stickyFooter,
  overflowHidden,
  overflowAuto,
  relative,
  absoluteFill,
  appContainer,
  contentWrapper,
  section,
  cardGrid,
  formContainer,
  formRow,
  actionContainer,
  pageSection,
  tableWrapper,
  emptyState,
  modalContent,
  drawerContent,
  stickyTop,
  stickyBottom,
  scrollY,
  scrollX,
  fullScreenCenter,
  fullScreenColumn,
  grow,
  shrink,
  relativeContainer,
  absoluteCenter,
  absoluteTopRight,
  absoluteTopLeft,
  absoluteBottomRight,
  absoluteBottomLeft,
  sidebarItem,
  sidebarItemContent,
  sidebarSubMenu,
  sidebarLogoContainer,
  sidebarLogo,
  sidebarChevron,
};