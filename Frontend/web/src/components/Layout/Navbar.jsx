import { useState } from "react";
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

import useAuth from "../../hooks/useAuth";

import "../../styles/Layout/navbar.css";

const Navbar = () => {
  const { logout, user } = useAuth();

  const [selectedBranch, setSelectedBranch] = useState("main");

  return (
    <Flex className="navbar">
      {/* =========================
          SEARCH
      ========================= */}

      <Box className="navbar-search">
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <FaSearch className="navbar-search-icon" />
          </InputLeftElement>

          <Input
            className="navbar-input"
            placeholder="Search anything..."
          />
        </InputGroup>
      </Box>

      {/* =========================
          RIGHT SIDE
      ========================= */}

      <HStack spacing={4}>
        {/* Branch Selector */}

        <Box className="navbar-branch">
          <Select
            className="navbar-select"
            value={selectedBranch}
            onChange={(e) =>
              setSelectedBranch(e.target.value)
            }
          >
            <option value="main">Main Branch</option>

            <option value="bbsr">
              Bhubaneswar Branch
            </option>

            <option value="ctc">
              Cuttack Branch
            </option>

            <option value="puri">
              Puri Branch
            </option>

            <option value="berhampur">
              Berhampur Branch
            </option>
          </Select>
        </Box>

        {/* Notification */}

        <IconButton
          className="navbar-bell"
          icon={<FaBell />}
          aria-label="Notifications"
          variant="ghost"
        />

        {/* User */}

        <Menu>
          <MenuButton>
            <HStack
              spacing={3}
              className="navbar-user"
            >
              <Avatar
                size="sm"
                name={user?.name || "Admin"}
              />

              <Box>
                <Text className="navbar-name">
                  {user?.name || "Admin"}
                </Text>

                <Text className="navbar-role">
                  {user?.role || "Super Admin"}
                </Text>
              </Box>
            </HStack>
          </MenuButton>

          <MenuList className="navbar-menu">
            <MenuItem>Profile</MenuItem>

            <MenuItem>Settings</MenuItem>

            <MenuItem
              color="red.500"
              onClick={logout}
            >
              Logout
            </MenuItem>
          </MenuList>
        </Menu>
      </HStack>
    </Flex>
  );
};

export default Navbar;