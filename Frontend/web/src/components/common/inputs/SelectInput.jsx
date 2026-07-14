import { Select } from "@chakra-ui/react";
import { selectInput } from "../../../styles/components/inputs";

const SelectInput = ({ children, sx = {}, ...props }) => {
  return (
    <Select
      sx={{
        ...selectInput,
        ...sx,
      }}
      {...props}
    >
      {children}
    </Select>
  );
};

export default SelectInput;
