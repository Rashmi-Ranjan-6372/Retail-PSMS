import { InputGroup, InputLeftElement } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";

import TextInput from "./TextInput";

import { searchInput, inputAction } from "../../../styles/components/inputs";

const SearchInput = ({ sx = {}, ...props }) => {
  return (
    <InputGroup>
      <InputLeftElement pointerEvents="none">
        <SearchIcon sx={inputAction} />
      </InputLeftElement>

      <TextInput
        sx={{
          ...searchInput,
          ...sx,
        }}
        {...props}
      />
    </InputGroup>
  );
};

export default SearchInput;
