import { FormLabel } from "@chakra-ui/react";
import { inputLabel } from "../../../styles/components/inputs";

const Label = ({ children, required = false, sx = {}, ...props }) => {
  return (
    <FormLabel
      sx={{
        ...inputLabel,
        ...sx,
      }}
      {...props}
    >
      {children}
      {required && <span style={{ color: "#E53E3E", marginLeft: 4 }}>*</span>}
    </FormLabel>
  );
};

export default Label;
