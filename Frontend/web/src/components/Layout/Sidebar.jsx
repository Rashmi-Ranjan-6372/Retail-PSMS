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

const hasActiveChild = (menu, pathname) => {
  if (!menu.children) return false;

  return menu.children.some(
    (child) =>
      child.path === pathname ||
      (child.children && hasActiveChild(child, pathname))
  );
};

const isMenuActive = (menu, pathname) => {
  return (
    menu.path === pathname ||
    (menu.children && hasActiveChild(menu, pathname))
  );
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

const MenuItem = ({
  item,
  level,
  pathname,
  navigate,
  openedMenus,
  setOpenedMenus,
}) => {
  const hasChildren = item.children?.length > 0;

  const isOpen = openedMenus.includes(item.id);

  const isActive = isMenuActive(item, pathname);

  const textColor = useColorModeValue("gray.700", "gray.100");
  const hoverColor = useColorModeValue("gray.100", "gray.700");

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
        borderRadius="10px"
        transition=".2s"
        bg={isActive ? "blue.600" : "transparent"}
        color={isActive ? "white" : textColor}
        _hover={{
          bg: isActive ? "blue.600" : hoverColor,
        }}
        onClick={() => {
          if (hasChildren) toggleMenu();
          else navigate(item.path);
        }}
      >
        <Flex align="center" gap={3}>
          {item.icon && (
            <Icon
              as={item.icon}
              boxSize={4}
            />
          )}

          <Text
            fontSize="sm"
            fontWeight="600"
          >
            {item.label}
          </Text>
        </Flex>

        {hasChildren && (
          <Icon
            as={isOpen ? FaChevronUp : FaChevronDown}
            fontSize="12px"
          />
        )}
      </Flex>

      {hasChildren && (
        <Collapse in={isOpen}>
          <VStack
            spacing={1}
            mt={1}
            align="stretch"
          >
            {item.children.map((child, index) => (
              <MenuItem
                key={
                  child.id ??
                  child.path ??
                  `${item.id}-${index}`
                }
                item={child}
                level={level + 1}
                pathname={pathname}
                navigate={navigate}
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

const Sidebar = () => {
  const { role, user } = useAuth();
  
  const navigate = useNavigate();

  const { pathname } = useLocation();

  const bg = useColorModeValue("white", "gray.900");

  const border = useColorModeValue("gray.200", "gray.700");

  const sidebarMenus = useMemo(() => {
    if (!role) return [];

    return getSidebarByRole(role);
  }, [role]);

  const defaultOpened = useMemo(
    () => getDefaultOpenMenus(sidebarMenus, pathname),
    [sidebarMenus, pathname]
  );

  const [openedMenus, setOpenedMenus] = useState(defaultOpened);

  useEffect(() => {
    setOpenedMenus(defaultOpened);
  }, [defaultOpened]);

  return (
    <Box
      w="280px"
      h="100vh"
      bg={bg}
      borderRight="1px solid"
      borderColor={border}
      position="sticky"
      top={0}
      overflow="hidden"
    >
      <Flex
        h="90px"
        justify="center"
        align="center"
        borderBottom="1px solid"
        borderColor={border}
      >
        <Image
          src="/logo.png"
          w="170px"
          objectFit="contain"
        />
      </Flex>

      <Box
        h="calc(100vh - 90px)"
        overflowY="auto"
        px={3}
        py={4}
      >
        <VStack
          align="stretch"
          spacing={2}
        >
          {sidebarMenus.map((menu, index) => (
            <MenuItem
              key={
                menu.id ??
                menu.path ??
                `menu-${index}`
              }
              item={menu}
              level={0}
              pathname={pathname}
              navigate={navigate}
              openedMenus={openedMenus}
              setOpenedMenus={setOpenedMenus}
            />
          ))}
        </VStack>
      </Box>
    </Box>
  );
};

export default Sidebar;