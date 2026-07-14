import { Textarea } from "@chakra-ui/react";
import { textArea } from "../../../styles/components/inputs";

const TextArea = ({ sx = {}, ...props }) => {
  return (
    <Textarea
      sx={{
        ...textArea,
        ...sx,
      }}
      {...props}
    />
  );
};

export default TextArea;
