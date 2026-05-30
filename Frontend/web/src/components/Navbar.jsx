import {
  Flex,
  Input,
  InputGroup,
  InputLeftElement,
  IconButton,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  HStack,
  Text,
  Box,
  Select,
} from "@chakra-ui/react";

import { FaBell, FaSearch } from "react-icons/fa";

import { useState } from "react";
import useAuth from "../hooks/useAuth";

const Navbar = () => {
  const { logout } = useAuth();

  const [selectedBranch, setSelectedBranch] = useState("main");

  return (
    <Flex
      h="70px"
      bg="white"
      px={6}
      align="center"
      justify="space-between"
      borderBottom="1px solid"
      borderColor="gray.200"
      boxShadow="sm"
      position="sticky"
      top="0"
      zIndex="sticky"
      backdropFilter="blur(10px)"
    >
      {/* Search */}
      <Box w="400px">
        <InputGroup>
          <InputLeftElement>
            <FaSearch color="gray" />
          </InputLeftElement>

          <Input placeholder="Search..." bg="gray.50" borderRadius="xl" />
        </InputGroup>
      </Box>

      {/* Right Side */}
      <HStack spacing={4}>
        {/* Branch Selector */}
        <Box minW="220px">
          <Select
            value={selectedBranch}
            onChange={(e) => setSelectedBranch(e.target.value)}
            borderRadius="xl"
            bg="gray.50"
          >
            <option value="main">Main Branch</option>

            <option value="bbsr">Bhubaneswar Branch</option>

            <option value="ctc">Cuttack Branch</option>

            <option value="puri">Puri Branch</option>

            <option value="berhampur">Berhampur Branch</option>
          </Select>
        </Box>

        {/* Notification */}
        <IconButton
          icon={<FaBell />}
          variant="ghost"
          aria-label="notification"
          size="lg"
        />

        {/* User Menu */}
        <Menu>
          <MenuButton>
            <HStack spacing={3}>
              <Avatar size="sm" name="Admin User" />

              <Box textAlign="left">
                <Text fontSize="sm" fontWeight="bold">
                  Admin
                </Text>

                <Text fontSize="xs" color="gray.500">
                  Super Admin
                </Text>
              </Box>
            </HStack>
          </MenuButton>

          <MenuList>
            <MenuItem>Profile</MenuItem>

            <MenuItem>Settings</MenuItem>

            <MenuItem color="red.500" onClick={logout}>
              Logout
            </MenuItem>
          </MenuList>
        </Menu>
      </HStack>
    </Flex>
  );
};

export default Navbar;
