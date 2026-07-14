import { Box } from "@chakra-ui/react";
import { modalCard } from "../../../styles/components/cards";

const ModalCard = ({ children, ...props }) => {
  return (
    <Box sx={modalCard} {...props}>
      {children}
    </Box>
  );
};

export default ModalCard;
