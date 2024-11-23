import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { EssayPlan, essayPlanService } from '../../services/essayPlanService';
import { useNavigate } from 'react-router-dom';

export const EssayPlanList: React.FC = () => {
  const [plans, setPlans] = useState<EssayPlan[]>([]);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<EssayPlan | null>(null);
  const navigate = useNavigate();

  const loadPlans = async () => {
    try {
      const data = await essayPlanService.getUserPlans();
      setPlans(data);
    } catch (error) {
      console.error('Error loading essay plans:', error);
    }
  };

  useEffect(() => {
    loadPlans();
  }, []);

  const handleCreateNew = () => {
    navigate('/essay-plans/new');
  };

  const handleEdit = (planId: number) => {
    navigate(`/essay-plans/${planId}/edit`);
  };

  const handleDeleteClick = (plan: EssayPlan) => {
    setSelectedPlan(plan);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (selectedPlan) {
      try {
        await essayPlanService.deletePlan(selectedPlan.id);
        await loadPlans();
      } catch (error) {
        console.error('Error deleting essay plan:', error);
      }
    }
    setDeleteDialogOpen(false);
    setSelectedPlan(null);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Essay Plans</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleCreateNew}
        >
          Create New Plan
        </Button>
      </Box>

      <Grid container spacing={3}>
        {plans.map((plan) => (
          <Grid item xs={12} sm={6} md={4} key={plan.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {plan.title}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  {plan.essayType}
                </Typography>
                <Typography variant="body2" noWrap>
                  {plan.topic}
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                  <IconButton onClick={() => handleEdit(plan.id)} size="small">
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDeleteClick(plan)} size="small" color="error">
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Essay Plan</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete "{selectedPlan?.title}"? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
