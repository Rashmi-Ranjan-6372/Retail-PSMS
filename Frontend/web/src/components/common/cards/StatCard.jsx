import { Box } from "@chakra-ui/react";
import { statCard } from "../../../styles/components/cards";

const StatCard = ({ children, ...props }) => {
  return (
    <Box sx={statCard} {...props}>
      {children}
    </Box>
  );
};

export default StatCard;
