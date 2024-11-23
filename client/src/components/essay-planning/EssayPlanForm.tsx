import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  MenuItem,
  Grid,
  Typography,
  Paper,
  IconButton,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import {
  EssayPlan,
  CreateEssayPlanDto,
  UpdateEssayPlanDto,
  essayPlanService,
} from '../../services/essayPlanService';

const ESSAY_TYPES = [
  'Argumentative',
  'Analytical',
  'Expository',
  'Descriptive',
  'Narrative',
  'Persuasive',
  'Comparative',
];

interface OutlineSection {
  id: string;
  title: string;
  content: string;
}

export const EssayPlanForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = Boolean(id);

  const [formData, setFormData] = useState<CreateEssayPlanDto>({
    title: '',
    essayType: '',
    topic: '',
    thesisStatement: '',
    outline: { sections: [] },
    guidelines: {},
    wordCountTarget: undefined,
  });

  const [sections, setSections] = useState<OutlineSection[]>([]);

  useEffect(() => {
    if (isEditing) {
      loadPlan();
    }
  }, [id]);

  const loadPlan = async () => {
    try {
      const plan = await essayPlanService.getPlan(Number(id));
      setFormData({
        title: plan.title,
        essayType: plan.essayType,
        topic: plan.topic,
        thesisStatement: plan.thesisStatement,
        outline: plan.outline,
        guidelines: plan.guidelines,
        wordCountTarget: plan.wordCountTarget,
      });
      setSections(plan.outline.sections || []);
    } catch (error) {
      console.error('Error loading essay plan:', error);
      navigate('/essay-plans');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleAddSection = () => {
    const newSection: OutlineSection = {
      id: Date.now().toString(),
      title: '',
      content: '',
    };
    setSections((prev) => [...prev, newSection]);
  };

  const handleRemoveSection = (id: string) => {
    setSections((prev) => prev.filter((section) => section.id !== id));
  };

  const handleSectionChange = (id: string, field: keyof OutlineSection, value: string) => {
    setSections((prev) =>
      prev.map((section) =>
        section.id === id ? { ...section, [field]: value } : section
      )
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const planData = {
      ...formData,
      outline: { sections },
    };

    try {
      if (isEditing) {
        await essayPlanService.updatePlan(Number(id), planData as UpdateEssayPlanDto);
      } else {
        await essayPlanService.createPlan(planData as CreateEssayPlanDto);
      }
      navigate('/essay-plans');
    } catch (error) {
      console.error('Error saving essay plan:', error);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        {isEditing ? 'Edit Essay Plan' : 'Create New Essay Plan'}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            required
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            select
            label="Essay Type"
            name="essayType"
            value={formData.essayType}
            onChange={handleInputChange}
            required
          >
            {ESSAY_TYPES.map((type) => (
              <MenuItem key={type} value={type}>
                {type}
              </MenuItem>
            ))}
          </TextField>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="Word Count Target"
            name="wordCountTarget"
            type="number"
            value={formData.wordCountTarget || ''}
            onChange={handleInputChange}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Topic"
            name="topic"
            value={formData.topic}
            onChange={handleInputChange}
            required
            multiline
            rows={2}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Thesis Statement"
            name="thesisStatement"
            value={formData.thesisStatement}
            onChange={handleInputChange}
            multiline
            rows={3}
          />
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6">Outline</Typography>
              <Button startIcon={<AddIcon />} onClick={handleAddSection}>
                Add Section
              </Button>
            </Box>

            {sections.map((section) => (
              <Box key={section.id} sx={{ mb: 2 }}>
                <Grid container spacing={2}>
                  <Grid item xs={11}>
                    <TextField
                      fullWidth
                      label="Section Title"
                      value={section.title}
                      onChange={(e) =>
                        handleSectionChange(section.id, 'title', e.target.value)
                      }
                      sx={{ mb: 1 }}
                    />
                    <TextField
                      fullWidth
                      label="Content"
                      value={section.content}
                      onChange={(e) =>
                        handleSectionChange(section.id, 'content', e.target.value)
                      }
                      multiline
                      rows={2}
                    />
                  </Grid>
                  <Grid item xs={1}>
                    <IconButton
                      color="error"
                      onClick={() => handleRemoveSection(section.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Grid>
                </Grid>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
        <Button variant="contained" color="primary" type="submit">
          {isEditing ? 'Save Changes' : 'Create Plan'}
        </Button>
        <Button variant="outlined" onClick={() => navigate('/essay-plans')}>
          Cancel
        </Button>
      </Box>
    </Box>
  );
};
