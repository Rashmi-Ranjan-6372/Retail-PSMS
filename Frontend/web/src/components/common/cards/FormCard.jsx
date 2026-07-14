import { Box } from "@chakra-ui/react";
import { formCard } from "../../../styles/components/cards";

const FormCard = ({ children, ...props }) => {
  return (
    <Box sx={formCard} {...props}>
      {children}
    </Box>
  );
};

export default FormCard;
