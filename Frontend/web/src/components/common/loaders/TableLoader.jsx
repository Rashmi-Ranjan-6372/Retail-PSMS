import { Box, Skeleton } from "@chakra-ui/react";
import {
  tableLoader,
  tableSkeleton,
  skeleton,
} from "../../../styles/components/loaders";

const TableLoader = ({ rows = 6 }) => {
  return (
    <Box sx={tableLoader}>
      <Box sx={tableSkeleton}>
        {[...Array(rows)].map((_, index) => (
          <Skeleton key={index} height="45px" sx={skeleton} />
        ))}
      </Box>
    </Box>
  );
};

export default TableLoader;
