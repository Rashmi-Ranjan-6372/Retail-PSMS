import { Box, Spinner } from "@chakra-ui/react";
import { fullScreenLoader, spinner } from "../../styles/common";

const FullScreenLoader = () => {
  return (
    <Box sx={fullScreenLoader}>
      <Spinner
        size="xl"
        thickness={spinner.thickness}
        speed={spinner.speed}
        emptyColor={spinner.emptyColor}
        color={spinner.color}
      />
    </Box>
  );
};

export default FullScreenLoader;