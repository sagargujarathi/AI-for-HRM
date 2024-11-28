import { useState } from "react";
import { Container, TextField, Button, Typography, Box } from "@mui/material";
import axios from "axios";

const Dashboard = () => {
  const [officerData, setOfficerData] = useState({
    Branch: "",
    Stream: "",
    PromotionsGazetted: "",
    TrainingCourses: "",
    BadgesQualified: "",
    Awards: "",
  });
  const [recommendation, setRecommendation] = useState("");

  const handleChange = (e) => {
    setOfficerData({
      ...officerData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/recommend_posting",
        officerData
      );
      setRecommendation(response.data.recommended_posting);
    } catch (error) {
      console.error("Error fetching recommendation:", error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          HRM Dashboard
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Branch"
            name="Branch"
            value={officerData.Branch}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Stream"
            name="Stream"
            value={officerData.Stream}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Promotions Gazetted"
            name="PromotionsGazetted"
            value={officerData.PromotionsGazetted}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Training Courses"
            name="TrainingCourses"
            value={officerData.TrainingCourses}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Badges Qualified"
            name="BadgesQualified"
            value={officerData.BadgesQualified}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Awards"
            name="Awards"
            value={officerData.Awards}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
          >
            Get Recommendation
          </Button>
        </form>
        {recommendation && (
          <Typography variant="h6" color="secondary" sx={{ mt: 4 }}>
            Recommended Posting: {recommendation}
          </Typography>
        )}
      </Box>
    </Container>
  );
};

export default Dashboard;
