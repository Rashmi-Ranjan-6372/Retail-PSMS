import {
  Box,
  VStack,
  Text,
  Collapse,
  Flex,
  Icon,
  Image,
  Divider,
} from "@chakra-ui/react";

import {
  FaTachometerAlt,
  FaBoxes,
  FaCapsules,
  FaIndustry,
  FaTruck,
  FaUserFriends,
  FaDollarSign,
  FaWarehouse,
  FaUndo,
  FaClock,
  FaMoneyCheckAlt,
  FaFileInvoice,
  FaFileInvoiceDollar,
  FaBook,
  FaUserTie,
  FaCog,
  FaCalendarCheck,
  FaMapMarkedAlt,
  FaChevronDown,
  FaChevronUp,
} from "react-icons/fa";

import { FaChartColumn } from "react-icons/fa6";

import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";

const sidebarStructure = [
  {
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  {
    label: "Masters",
    icon: FaBoxes,
    items: [
      {
        label: "Products",
        icon: FaCapsules,
        path: "/masters/products",
      },
      {
        label: "Categories",
        icon: FaBoxes,
        path: "/masters/categories",
      },
      {
        label: "Manufacturers",
        icon: FaIndustry,
        path: "/masters/manufacturers",
      },
      {
        label: "Suppliers",
        icon: FaTruck,
        path: "/masters/suppliers",
      },
      {
        label: "Customers",
        icon: FaUserFriends,
        path: "/masters/customers",
      },
      {
        label: "Sales Offers",
        icon: FaDollarSign,
        path: "/masters/sales-offers",
      },
    ],
  },

  {
    label: "Inventory",
    icon: FaWarehouse,
    items: [
      {
        label: "Stock Transactions",
        icon: FaBoxes,
        path: "/inventory/stock-transactions",
      },
      {
        label: "Stock Batches",
        icon: FaBoxes,
        path: "/inventory/stock-batches",
      },
      {
        label: "Stock Adjustments",
        icon: FaUndo,
        path: "/inventory/stock-adjustments",
      },
      {
        label: "Stock Transfers",
        icon: FaUndo,
        path: "/inventory/stock-transfers",
      },
      {
        label: "Expiry Damages",
        icon: FaClock,
        path: "/inventory/expiry-damages",
      },
    ],
  },

  {
    label: "Purchases",
    icon: FaTruck,
    items: [
      {
        label: "Purchases",
        icon: FaFileInvoice,
        path: "/purchases",
      },
      {
        label: "Purchase Returns",
        icon: FaUndo,
        path: "/purchase-returns",
      },
      {
        label: "Payments",
        icon: FaMoneyCheckAlt,
        path: "/payments",
      },
    ],
  },

  {
    label: "Sales",
    icon: FaDollarSign,
    items: [
      {
        label: "Sales",
        icon: FaFileInvoiceDollar,
        path: "/sales",
      },
      {
        label: "Sales Returns",
        icon: FaUndo,
        path: "/sales-returns",
      },
      {
        label: "Receipts",
        icon: FaMoneyCheckAlt,
        path: "/receipts",
      },
    ],
  },

  {
    label: "Reports",
    icon: FaChartColumn,
    items: [
      {
        label: "Sales Report",
        icon: FaFileInvoice,
        path: "/reports/sales",
      },
      {
        label: "Purchase Report",
        icon: FaTruck,
        path: "/reports/purchases",
      },
      {
        label: "Stock Report",
        icon: FaWarehouse,
        path: "/reports/stock",
      },
      {
        label: "Profit & Loss",
        icon: FaDollarSign,
        path: "/reports/profit-loss",
      },
    ],
  },

  {
    label: "Branch Management",
    icon: FaMapMarkedAlt,
    items: [
      {
        label: "Branches",
        icon: FaMapMarkedAlt,
        path: "/branches",
      },
    ],
  },

  {
    label: "User Management",
    icon: FaUserFriends,
    items: [
      {
        label: "Users",
        icon: FaUserFriends,
        path: "/users",
      },
      {
        label: "User Sessions",
        icon: FaClock,
        path: "/users/sessions",
      },
      {
        label: "Login Logs",
        icon: FaClock,
        path: "/users/login-logs",
      },
      {
        label: "Audit Logs",
        icon: FaBook,
        path: "/users/audit-logs",
      },
    ],
  },

  {
    label: "Settings",
    icon: FaCog,
    items: [
      {
        label: "General Settings",
        icon: FaCog,
        path: "/settings/general",
      },
      {
        label: "Financial Years",
        icon: FaCalendarCheck,
        path: "/settings/financial-years",
      },
    ],
  },
];

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [openMenu, setOpenMenu] = useState("Masters");

  const toggleMenu = (label) => {
    setOpenMenu(openMenu === label ? null : label);
  };

  return (
    <Box
      w="270px"
      h="100vh"
      bg="white"
      borderRight="1px solid"
      borderColor="gray.200"
      boxShadow="sm"
      position="sticky"
      top="0"
    >
      {/* Sticky Logo */}
      <Box position="sticky" top="0" zIndex="100" bg="white">
        <Flex justify="center" align="center" py={6}>
          <Image
            src="/logo.png"
            alt="Logo"
            w="160px"
            h="auto"
            objectFit="contain"
          />
        </Flex>
      </Box>

      {/* Scrollable Menu */}
      <Box h="calc(100vh - 110px)" overflowY="auto" p={3}>
        <VStack align="stretch" spacing={2}>
          {sidebarStructure.map((menu, index) => {
            const isOpen = openMenu === menu.label;

            if (menu.items) {
              return (
                <Box key={index}>
                  <Flex
                    align="center"
                    justify="space-between"
                    p={3}
                    borderRadius="xl"
                    cursor="pointer"
                    color="gray.700"
                    _hover={{
                      bg: "gray.100",
                    }}
                    onClick={() => toggleMenu(menu.label)}
                  >
                    <Flex align="center" gap={3}>
                      <Icon as={menu.icon} boxSize={5} />
                      <Text fontWeight="500">{menu.label}</Text>
                    </Flex>

                    <Icon as={isOpen ? FaChevronUp : FaChevronDown} />
                  </Flex>

                  <Collapse in={isOpen}>
                    <VStack align="stretch" pl={5} mt={1} spacing={1}>
                      {menu.items.map((subMenu, subIndex) => (
                        <Flex
                          key={subIndex}
                          align="center"
                          gap={3}
                          p={3}
                          borderRadius="xl"
                          cursor="pointer"
                          bg={
                            location.pathname === subMenu.path
                              ? "blue.600"
                              : "transparent"
                          }
                          color={
                            location.pathname === subMenu.path
                              ? "white"
                              : "gray.600"
                          }
                          _hover={{
                            bg:
                              location.pathname === subMenu.path
                                ? "blue.600"
                                : "gray.100",
                          }}
                          onClick={() => navigate(subMenu.path)}
                        >
                          <Icon as={subMenu.icon} />
                          <Text fontSize="sm" fontWeight="500">
                            {subMenu.label}
                          </Text>
                        </Flex>
                      ))}
                    </VStack>
                  </Collapse>
                </Box>
              );
            }

            return (
              <Flex
                key={index}
                align="center"
                gap={3}
                p={3}
                borderRadius="xl"
                cursor="pointer"
                bg={
                  location.pathname === menu.path ? "blue.600" : "transparent"
                }
                color={location.pathname === menu.path ? "white" : "gray.700"}
                _hover={{
                  bg: location.pathname === menu.path ? "blue.600" : "gray.100",
                }}
                onClick={() => navigate(menu.path)}
              >
                <Icon as={menu.icon} boxSize={5} />
                <Text fontWeight="500">{menu.label}</Text>
              </Flex>
            );
          })}
        </VStack>
      </Box>
    </Box>
  );
};

export default Sidebar;
