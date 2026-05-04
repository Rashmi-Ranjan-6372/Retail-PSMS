import { Flex, Text, Button } from "@chakra-ui/react";
import useAuth from "../hooks/useAuth";

const Navbar = () => {
  const { logout } = useAuth();

  return (
    <Flex
      h="60px"
      bg="blue.500"
      color="white"
      align="center"
      justify="space-between"
      px={5}
    >
      <Text fontSize="lg" fontWeight="bold">
        Pharmacy System
      </Text>

      <Button colorScheme="red" size="sm" onClick={logout}>
        Logout
      </Button>
    </Flex>
  );
};

export default Navbar;