import { Box, Spinner } from "@chakra-ui/react";
import { loaderContainer, spinner } from "../../styles/common";

const Loader = ({ size = "lg" }) => {
  return (
    <Box sx={loaderContainer}>
      <Spinner
        size={size}
        thickness={spinner.thickness}
        speed={spinner.speed}
        emptyColor={spinner.emptyColor}
        color={spinner.color}
      />
    </Box>
  );
};

export default Loader;