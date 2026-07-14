import { Spinner as ChakraSpinner } from "@chakra-ui/react";
import { spinner } from "../../../styles/components/loaders";

const Spinner = (props) => {
  return <ChakraSpinner sx={spinner} {...props} />;
};

export default Spinner;
