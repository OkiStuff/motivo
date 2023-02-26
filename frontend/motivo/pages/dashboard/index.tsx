import { Button, Flex, Heading, Input, useColorMode, useColorModeValue, Link, Center } from '@chakra-ui/react'

export default function Home() {
  const { toggleColorMode } = useColorMode()
  const formBackground = useColorModeValue("gray.100", "gray.700")

  return (
    <Flex h="100vh" alignItems="center" justifyContent="center">
      <Flex direction="column" background={formBackground} p={12} rounded={6}>
        <Heading mb={6}>Motivo</Heading>
        <Input placeholder='joe@example.com' variant="filled" mb={3} type="email" />
        <Input placeholder='*********' variant={"filled"} mb={3} type="password" />
        <Button mb={6} colorScheme={"teal"}>Log In</Button>
        <Button mb={2} onClick={toggleColorMode}>Toggle Color Mode</Button>
        <Center>
          <Link>Create an account</Link>
        </Center>
      </Flex>
    </Flex>
  )
}