import { config } from '@/globals/api'
import { Button, Flex, Heading, Input, useColorMode, useColorModeValue, Link, Center, Stack } from '@chakra-ui/react'
import { useRouter } from 'next/router'
import React from 'react'

export default function Home() {
  const { toggleColorMode } = useColorMode()
  const router = useRouter();
  const formBackground = useColorModeValue("gray.100", "gray.700")

  const [ emailValue, setEmailValue ] = React.useState('')
  const [ passwordValue, setPasswordValue ] = React.useState('')
  const [ usernameValue, setUsernameValue ] = React.useState('')
  const [ streakMinValue, setStreakMinValue ] = React.useState(0.80)

  let errorMessage: null | String = null;

  return (
    <Flex h="100vh" alignItems="center" justifyContent="center">
      <Flex direction="column" background={formBackground} p={12} rounded={6}>
        <Heading mb={6}>Motivo</Heading>
        <Input placeholder='joe@example.com' onChange={(event) => {setEmailValue(event.target.value)}} variant="filled" mb={3} type="email" />
        <Input placeholder='Joe Smith' onChange={(event) => {setUsernameValue(event.target.value)}} variant="filled" mb={3} type="text"/>
        <Input placeholder='*********' onChange={(event) => {setPasswordValue(event.target.value)}} variant={"filled"} mb={3} type="password" />
        
        <Center mb={3}>
            <h4>Streak Percantage Minimum</h4>
        </Center>

        <Stack spacing={4} mb={3}direction='row' align='center'>
            <Button onClick={(event) => {setStreakMinValue(0.60)}} colorScheme={ streakMinValue === 0.60 ? "blue" : "gray" }>
                60%
            </Button>

            <Button onClick={(event) => {setStreakMinValue(0.70)}} colorScheme={ streakMinValue ===  0.70 ? "blue" : "gray" }>
                70%
            </Button>

            <Button onClick={(event) => {setStreakMinValue(0.80)}} colorScheme={ streakMinValue === 0.80 ? "blue" : "gray" }>
                80%
            </Button>
        </Stack>
        
        <Button mb={6} colorScheme={"teal"} onClick={() => {
            let response_status: Number;

            fetch(`${config.api_url}/users/new`, {
                method: "POST",
                body: JSON.stringify({
                    email: emailValue,
                    password: passwordValue,
                    username: usernameValue,
                    streak_min: streakMinValue
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then((response) => {
                    response_status = response.status;
                    return response.text()
                })
                .then((text) => {
                    if (response_status === 200) {
                        JSON.parse(text).user.id
                    }
                })
                
        }}>Sign Up</Button>

            <p color='red'>{errorMessage != null ? errorMessage : ""}</p>

        <Button mb={2} onClick={toggleColorMode}>Toggle Color Mode</Button>
        <Center>
          <Link href="/">Log In</Link>
        </Center>
      </Flex>
    </Flex>
  )
}
