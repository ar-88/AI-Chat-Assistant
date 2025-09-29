
-- Simple knowledge base schema for AI Chat Assistant

DROP TABLE IF EXISTS knowledge;

CREATE TABLE knowledge (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL
);

-- Sample data
INSERT INTO knowledge (question, answer) VALUES
('What is your name?', 'I am your AI Chat Assistant.'),
('How can you help me?', 'I can answer your questions based on my knowledge base.'),
('What is AI?', 'AI stands for Artificial Intelligence, which enables machines to mimic human intelligence.'),
('Tell me a joke.', 'Why did the computer show up at work late? It had a hard drive!');
