import { Box, Skeleton } from "@chakra-ui/react";
import { dashboardLoader, skeleton } from "../../../styles/components/loaders";

const DashboardLoader = ({ count = 4 }) => {
  return (
    <Box sx={dashboardLoader}>
      {[...Array(count)].map((_, index) => (
        <Skeleton key={index} height="130px" sx={skeleton} />
      ))}
    </Box>
  );
};

export default DashboardLoader;
