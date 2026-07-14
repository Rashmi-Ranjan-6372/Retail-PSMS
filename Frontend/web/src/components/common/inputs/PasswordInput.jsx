import { useState } from "react";
import { InputGroup, InputRightElement, IconButton } from "@chakra-ui/react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

import TextInput from "./TextInput";
import { inputAction } from "../../../styles/components/inputs";

const PasswordInput = ({ sx = {}, ...props }) => {
  const [show, setShow] = useState(false);

  return (
    <InputGroup>
      <TextInput type={show ? "text" : "password"} sx={sx} {...props} />

      <InputRightElement h="100%">
        <IconButton
          variant="ghost"
          size="sm"
          icon={show ? <ViewOffIcon /> : <ViewIcon />}
          onClick={() => setShow(!show)}
          sx={inputAction}
          aria-label="Toggle Password"
        />
      </InputRightElement>
    </InputGroup>
  );
};

export default PasswordInput;
