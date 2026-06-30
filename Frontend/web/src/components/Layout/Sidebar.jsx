import React, { useMemo, useState, useEffect } from "react";
import {
  Box,
  Flex,
  Icon,
  Text,
  VStack,
  Collapse,
  Image,
  useColorModeValue,
} from "@chakra-ui/react";

import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { useNavigate, useLocation } from "react-router-dom";
import { getSidebarByRole } from "../../config/navigation";
import useAuth from "../../hooks/useAuth";

/*
|--------------------------------------------------------------------------
| Recursive Menu Component
|--------------------------------------------------------------------------
*/

const hasActiveChild = (menu, pathname) => {
  if (!menu.children) return false;

  for (const child of menu.children) {
    if (child.path === pathname) return true;
    if (child.children && hasActiveChild(child, pathname)) return true;
  }

  return false;
};

const isMenuActive = (menu, pathname) => {
  if (menu.path === pathname) return true;
  if (menu.children) return hasActiveChild(menu, pathname);
  return false;
};

const getDefaultOpenMenus = (menus, pathname) => {
  let opened = [];

  menus.forEach((menu) => {
    if (menu.children) {
      if (hasActiveChild(menu, pathname)) {
        opened.push(menu.id);
      }

      opened = [
        ...opened,
        ...getDefaultOpenMenus(menu.children, pathname),
      ];
    }
  });

  return opened;
};

/*
|--------------------------------------------------------------------------
| Menu Item
|--------------------------------------------------------------------------
*/

const MenuItem = ({
  item,
  level = 0,
  navigate,
  pathname,
  openedMenus,
  setOpenedMenus,
}) => {
  const hasChildren = item.children && item.children.length > 0;
  const isOpen = openedMenus.includes(item.id);
  const isActive = isMenuActive(item, pathname);

  const textColor = useColorModeValue("gray.700", "gray.100");
  const hoverColor = useColorModeValue("gray.100", "gray.700");
  const activeColor = "blue.600";

  const toggleMenu = () => {
    if (!hasChildren) return;

    setOpenedMenus((prev) =>
      isOpen
        ? prev.filter((id) => id !== item.id)
        : [...prev, item.id]
    );
  };

  return (
    <Box>
      <Flex
        align="center"
        justify="space-between"
        pl={`${level * 20 + 12}px`}
        pr="12px"
        py="12px"
        cursor="pointer"
        borderRadius="12px"
        transition="0.2s"
        bg={isActive ? activeColor : "transparent"}
        color={isActive ? "white" : textColor}
        _hover={{
          bg: isActive ? activeColor : hoverColor,
        }}
        onClick={() => {
          if (hasChildren) toggleMenu();
          else navigate(item.path);
        }}
      >
        <Flex align="center" gap={3}>
          {/* Active Indicator */}
          <Box
            w="4px"
            h="24px"
            borderRadius="full"
            bg={isActive ? "blue.400" : "transparent"}
          />

          {item.icon && <Icon as={item.icon} fontSize="18px" />}

          <Text fontSize="sm" fontWeight="600">
            {item.label}
          </Text>
        </Flex>

        {hasChildren && (
          <Icon
            as={isOpen ? FaChevronUp : FaChevronDown}
            fontSize="13px"
          />
        )}
      </Flex>

      {hasChildren && (
        <Collapse in={isOpen}>
          <VStack align="stretch" spacing={1} mt={1}>
            {item.children.map((child) => (
              <MenuItem
                key={child.id}
                item={child}
                level={level + 1}
                navigate={navigate}
                pathname={pathname}
                openedMenus={openedMenus}
                setOpenedMenus={setOpenedMenus}
              />
            ))}
          </VStack>
        </Collapse>
      )}
    </Box>
  );
};

/*
|--------------------------------------------------------------------------
| Sidebar Component
|--------------------------------------------------------------------------
*/

const Sidebar = () => {
  const { role } = useAuth(); // ✅ dynamic role

  const navigate = useNavigate();
  const location = useLocation();
  const pathname = location.pathname;

  const bgColor = useColorModeValue("white", "gray.900");
  const borderColor = useColorModeValue("gray.200", "gray.700");

  // ✅ FIX: role-safe sidebar generation
  const sidebarMenus = useMemo(() => {
    if (!role) return [];
    return getSidebarByRole(role);
  }, [role]);

  // Auto open active menus
  const defaultOpened = useMemo(() => {
    return getDefaultOpenMenus(sidebarMenus, pathname);
  }, [sidebarMenus, pathname]);

  const [openedMenus, setOpenedMenus] = useState(defaultOpened);

  useEffect(() => {
    setOpenedMenus(defaultOpened);
  }, [defaultOpened]);

  return (
    <Box
      w="280px"
      h="100vh"
      bg={bgColor}
      borderRight="1px solid"
      borderColor={borderColor}
      boxShadow="sm"
      position="sticky"
      top="0"
      overflow="hidden"
    >
      {/* Logo */}
      <Box
        position="sticky"
        top="0"
        bg={bgColor}
        zIndex="100"
        borderBottom="1px solid"
        borderColor="gray.100"
      >
        <Flex justify="center" align="center" h="90px" px={5}>
          <Image
            src="/logo.png"
            alt="Logo"
            w="170px"
            objectFit="contain"
            draggable={false}
          />
        </Flex>
      </Box>

      {/* Menu */}
      <Box h="calc(100vh - 90px)" overflowY="auto" px={3} py={4}>
        <VStack align="stretch" spacing={2}>
          {sidebarMenus.length > 0 ? (
            sidebarMenus.map((menu) => (
              <MenuItem
                key={menu.id}
                item={menu}
                level={0}
                navigate={navigate}
                pathname={pathname}
                openedMenus={openedMenus}
                setOpenedMenus={setOpenedMenus}
              />
            ))
          ) : (
            <Flex justify="center" align="center" py={10}>
              <Text fontSize="sm" color="gray.500">
                No Menu Available
              </Text>
            </Flex>
          )}
        </VStack>
      </Box>
    </Box>
  );
};

export default Sidebar;