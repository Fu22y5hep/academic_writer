import { useState } from 'react';
import {
  Paper,
  TextInput,
  Select,
  NumberInput,
  Button,
  Stack,
  Text,
  Accordion,
  Box,
  LoadingOverlay,
  Group
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { essayPlanService, type OutlineSection } from '../../services/essayPlanService';
import { isAuthenticated } from '../../utils/token';
import { AuthModal } from '../auth/AuthModal';
import { MIN_WORD_COUNT, DEFAULT_WORD_COUNT, MAX_WORD_COUNT } from '../../config';

const ESSAY_TYPES = [
  { value: 'argumentative', label: 'Argumentative' },
  { value: 'expository', label: 'Expository' },
  { value: 'analytical', label: 'Analytical' },
  { value: 'narrative', label: 'Narrative' },
  { value: 'compare-contrast', label: 'Compare and Contrast' },
  { value: 'research', label: 'Research Paper' }
];

interface OutlineSectionProps {
  section: OutlineSection;
  level?: number;
}

const OutlineSectionComponent: React.FC<OutlineSectionProps> = ({ section, level = 0 }) => {
  return (
    <Box ml={level * 20}>
      <Text weight={600} mb={5}>{section.title}</Text>
      <Text size="sm" mb={10} color="dimmed">{section.content}</Text>
      {section.subsections?.map((subsection, index) => (
        <OutlineSectionComponent
          key={index}
          section={subsection}
          level={level + 1}
        />
      ))}
    </Box>
  );
};

export function PlanningPanel() {
  const [topic, setTopic] = useState('');
  const [essayType, setEssayType] = useState<string | null>(null);
  const [wordCount, setWordCount] = useState<number | undefined>(DEFAULT_WORD_COUNT);
  const [thesisStatement, setThesisStatement] = useState('');
  const [loading, setLoading] = useState(false);
  const [outline, setOutline] = useState<OutlineSection[] | null>(null);
  const [authModalOpened, setAuthModalOpened] = useState(false);

  const handleGenerateOutline = async () => {
    if (!isAuthenticated()) {
      setAuthModalOpened(true);
      return;
    }

    if (!topic || !essayType) {
      notifications.show({
        title: 'Missing Information',
        message: 'Please provide both topic and essay type',
        color: 'red'
      });
      return;
    }

    setLoading(true);
    try {
      const response = await essayPlanService.generateOutline({
        topic,
        essay_type: essayType,
        word_count: wordCount,
        thesis_statement: thesisStatement || undefined
      });

      if (response.success && response.outline) {
        setOutline(response.outline.sections);
        notifications.show({
          title: 'Success',
          message: 'Outline generated successfully',
          color: 'green'
        });
      } else {
        notifications.show({
          title: 'Error',
          message: response.error || 'Failed to generate outline',
          color: 'red'
        });
      }
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'An unexpected error occurred',
        color: 'red'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Paper p="md" pos="relative">
        <LoadingOverlay visible={loading} blur={2} />
        <Stack spacing="md">
          <Group position="right">
            {!isAuthenticated() && (
              <Button onClick={() => setAuthModalOpened(true)}>
                Login to Generate Outlines
              </Button>
            )}
          </Group>

          <TextInput
            label="Topic"
            placeholder="Enter your essay topic"
            value={topic}
            onChange={(e) => setTopic(e.currentTarget.value)}
            required
          />

          <Select
            label="Essay Type"
            placeholder="Select essay type"
            data={ESSAY_TYPES}
            value={essayType}
            onChange={setEssayType}
            required
          />

          <NumberInput
            label="Word Count"
            placeholder="Enter target word count"
            value={wordCount}
            onChange={(value) => setWordCount(value || undefined)}
            min={MIN_WORD_COUNT}
            max={MAX_WORD_COUNT}
            step={100}
          />

          <TextInput
            label="Thesis Statement (Optional)"
            placeholder="Enter your thesis statement"
            value={thesisStatement}
            onChange={(e) => setThesisStatement(e.currentTarget.value)}
          />

          <Button onClick={handleGenerateOutline} disabled={!topic || !essayType}>
            Generate Outline
          </Button>

          {outline && (
            <Accordion defaultValue="outline" mt="md">
              <Accordion.Item value="outline">
                <Accordion.Control>Generated Outline</Accordion.Control>
                <Accordion.Panel>
                  <Stack spacing="sm">
                    {outline.map((section, index) => (
                      <OutlineSectionComponent key={index} section={section} />
                    ))}
                  </Stack>
                </Accordion.Panel>
              </Accordion.Item>
            </Accordion>
          )}
        </Stack>
      </Paper>

      <AuthModal
        opened={authModalOpened}
        onClose={() => setAuthModalOpened(false)}
      />
    </>
  );
}
