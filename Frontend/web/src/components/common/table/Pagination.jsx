import { Flex, Button, Text } from "@chakra-ui/react";

import { tablePagination } from "../../../styles/components/table";

import {
  primaryButton,
  secondaryButton,
} from "../../../styles/components/buttons";

const Pagination = ({ page = 1, totalPages = 1, onPageChange }) => {
  return (
    <Flex sx={tablePagination}>
      <Button
        sx={secondaryButton}
        size="sm"
        onClick={() => onPageChange(page - 1)}
        isDisabled={page === 1}
      >
        Previous
      </Button>

      <Text fontWeight="600">
        Page {page} of {totalPages}
      </Text>

      <Button
        sx={primaryButton}
        size="sm"
        onClick={() => onPageChange(page + 1)}
        isDisabled={page === totalPages}
      >
        Next
      </Button>
    </Flex>
  );
};

export default Pagination;
