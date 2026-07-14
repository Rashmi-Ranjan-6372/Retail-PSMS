import { Box } from "@chakra-ui/react";
import Spinner from "./Spinner";
import { pageLoader, loaderText } from "../../../styles/components/loaders";

const PageLoader = ({ text = "Loading..." }) => {
  return (
    <Box sx={pageLoader}>
      <Spinner />

      <Box sx={loaderText}>{text}</Box>
    </Box>
  );
};

export default PageLoader;
