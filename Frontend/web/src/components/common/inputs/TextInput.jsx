import { Input } from "@chakra-ui/react";
import { textInput } from "../../../styles/components/inputs";

const TextInput = ({ sx = {}, ...props }) => {
  return (
    <Input
      sx={{
        ...textInput,
        ...sx,
      }}
      {...props}
    />
  );
};

export default TextInput;
