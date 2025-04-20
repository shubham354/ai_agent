import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Flex,
  Input,
  Button,
  VStack,
  Text,
  useToast,
  IconButton,
  Divider,
} from '@chakra-ui/react';
import { FiSend, FiUpload } from 'react-icons/fi';
import axios from 'axios';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const toast = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        message: input,
      });

      const aiMessage: Message = {
        id: Date.now() + 1,
        text: response.data.message,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to get AI response',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const aiMessage: Message = {
        id: Date.now(),
        text: `Analysis complete! Here are the insights:\n${response.data.insights.join('\n')}`,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to analyze file',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box h="calc(100vh - 100px)" display="flex" flexDirection="column">
      <VStack flex="1" overflowY="auto" spacing={4} p={4}>
        {messages.map((message) => (
          <Flex
            key={message.id}
            alignSelf={message.sender === 'user' ? 'flex-end' : 'flex-start'}
            maxW="70%"
          >
            <Box
              bg={message.sender === 'user' ? 'blue.500' : 'gray.100'}
              color={message.sender === 'user' ? 'white' : 'black'}
              p={3}
              borderRadius="lg"
            >
              <Text>{message.text}</Text>
              <Text fontSize="xs" color={message.sender === 'user' ? 'white' : 'gray.500'}>
                {message.timestamp.toLocaleTimeString()}
              </Text>
            </Box>
          </Flex>
        ))}
        <div ref={messagesEndRef} />
      </VStack>
      <Divider />
      <Flex p={4} gap={2}>
        <Input
          flex="1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <IconButton
          aria-label="Upload file"
          icon={<FiUpload />}
          onClick={() => document.getElementById('file-upload')?.click()}
          isLoading={isLoading}
        />
        <input
          id="file-upload"
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileUpload}
          style={{ display: 'none' }}
        />
        <Button
          colorScheme="blue"
          onClick={handleSend}
          isLoading={isLoading}
          leftIcon={<FiSend />}
        >
          Send
        </Button>
      </Flex>
    </Box>
  );
};

export default Chat; 