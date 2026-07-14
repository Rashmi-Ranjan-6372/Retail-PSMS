import { Text as ChakraText } from "@chakra-ui/react";
import {
  bodyText,
  mutedText,
  smallText,
} from "../../../styles/common/typography";

const variants = {
  body: bodyText,
  muted: mutedText,
  small: smallText,
};

const Text = ({ children, variant = "body", sx = {}, ...props }) => {
  return (
    <ChakraText
      sx={{
        ...(variants[variant] || bodyText),
        ...sx,
      }}
      {...props}
    >
      {children}
    </ChakraText>
  );
};

export default Text;
