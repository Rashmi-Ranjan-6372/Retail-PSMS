import { Heading as ChakraHeading } from "@chakra-ui/react";
import {
  pageHeading,
  sectionHeading,
  cardHeading,
} from "../../../styles/common/typography";

const variants = {
  page: pageHeading,
  section: sectionHeading,
  card: cardHeading,
};

const Heading = ({ children, variant = "section", sx = {}, ...props }) => {
  return (
    <ChakraHeading
      sx={{
        ...(variants[variant] || sectionHeading),
        ...sx,
      }}
      {...props}
    >
      {children}
    </ChakraHeading>
  );
};

export default Heading;
