import { Box, VStack, Text } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const Sidebar = () => {
  const navigate = useNavigate();

  return (
    <Box
      w="220px"
      h="100vh"
      bg="gray.800"
      color="white"
      p={4}
    >
      <Text fontSize="xl" mb={6} fontWeight="bold">
        Menu
      </Text>

      <VStack align="start" spacing={4}>
        <Text cursor="pointer" onClick={() => navigate("/dashboard")}>
          Dashboard
        </Text>

        <Text cursor="pointer" onClick={() => navigate("/stock-entry")}>
          Stock Entry
        </Text>

        <Text cursor="pointer" onClick={() => navigate("/stock-list")}>
          Stock List
        </Text>
      </VStack>
    </Box>
  );
};

export default Sidebar;