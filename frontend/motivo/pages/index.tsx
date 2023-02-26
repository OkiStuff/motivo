import { Button, Flex, Heading, Input, useColorMode, useColorModeValue, Link, Center } from '@chakra-ui/react'
import { config } from '@/globals/api'
import React from 'react'

export default function Home() {
  const { toggleColorMode } = useColorMode()
  const formBackground = useColorModeValue("gray.100", "gray.700")

  const [ emailValue, setEmailValue ] = React.useState('')
  const [ passwordValue, setPasswordValue ] = React.useState('')

  return (
    <Flex h="100vh" alignItems="center" justifyContent="center">
      <Flex direction="column" background={formBackground} p={12} rounded={6}>
        <Heading mb={6}>Motivo</Heading>
        <Input placeholder='joe@example.com' onChange={(event) => {setEmailValue(event.target.value)}} variant="filled" mb={3} type="email" />
        <Input placeholder='*********' onChange={(event) => {setPasswordValue(event.target.value)}} variant={"filled"} mb={3} type="password" />
        <Button mb={6} onClick={() => {
          fetch(`${config.api_url}/users/auth`, {
            method: "POST",
            body: JSON.stringify({
              email: emailValue,
              password: passwordValue
            }),
            headers: {
              "Content-Type": "application/json",
            }
          })
            .then((response) => response.json())
            .then((data) => console.log(data));

        }}colorScheme={"teal"}>Log In</Button>
        <Button mb={2} onClick={toggleColorMode}>Toggle Color Mode</Button>
        <Center>
          <Link href="/signup">Create an account</Link>
        </Center>
      </Flex>
    </Flex>
  )
}
