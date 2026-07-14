import { Box } from "@chakra-ui/react";
import { dashboardCard } from "../../../styles/components/cards";

const DashboardCard = ({ children, ...props }) => {
  return (
    <Box sx={dashboardCard} {...props}>
      {children}
    </Box>
  );
};

export default DashboardCard;
