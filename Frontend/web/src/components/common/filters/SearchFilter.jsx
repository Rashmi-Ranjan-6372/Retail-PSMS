import { InputGroup, InputLeftElement } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";

import { searchWrapper } from "../../../styles/components/layout/navbar";
import { searchFilter } from "../../../styles/components/filters";
import { searchIcon } from "../../../styles/components/layout/navbar";

import TextInput from "../inputs/TextInput";

const SearchFilter = ({
  value,
  onChange,
  placeholder = "Search...",
  ...props
}) => {
  return (
    <InputGroup sx={searchWrapper}>
      <InputLeftElement pointerEvents="none">
        <SearchIcon sx={searchIcon} />
      </InputLeftElement>

      <TextInput
        sx={searchFilter}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        {...props}
      />
    </InputGroup>
  );
};

export default SearchFilter;
