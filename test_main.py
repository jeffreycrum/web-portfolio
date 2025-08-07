import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from main import (
    load_project_data,
    split_dataframe,
    render_header_section,
    render_intro_text,
    render_project_item,
    render_projects_section,
    main
)


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return """title,description,url,image
Project 1,Description 1,https://example1.com,1.png
Project 2,Description 2,https://example2.com,2.png
Project 3,Description 3,https://example3.com,3.png
Project 4,Description 4,https://example4.com,4.png"""


@pytest.fixture
def sample_dataframe():
    """Sample DataFrame for testing."""
    data = {
        'title': ['Project 1', 'Project 2', 'Project 3', 'Project 4'],
        'description': ['Desc 1', 'Desc 2', 'Desc 3', 'Desc 4'],
        'url': ['url1', 'url2', 'url3', 'url4'],
        'image': ['1.png', '2.png', '3.png', '4.png']
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_csv_file(sample_csv_data):
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(sample_csv_data)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


class TestLoadProjectData:
    """Tests for load_project_data function."""
    
    def test_load_project_data_success(self, temp_csv_file):
        """Test successful loading of CSV data."""
        df = load_project_data(temp_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert list(df.columns) == ['title', 'description', 'url', 'image']
        assert df.iloc[0]['title'] == 'Project 1'
    
    def test_load_project_data_default_path(self):
        """Test loading with default path."""
        with patch('pandas.read_csv') as mock_read_csv:
            mock_df = pd.DataFrame({'col1': [1, 2, 3]})
            mock_read_csv.return_value = mock_df
            
            result = load_project_data()
            
            mock_read_csv.assert_called_once_with("data.csv")
            assert result.equals(mock_df)
    
    def test_load_project_data_file_not_found(self):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_project_data("nonexistent.csv")
    
    def test_load_project_data_invalid_csv(self):
        """Test loading invalid CSV content - pandas handles malformed CSV gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("invalid,csv,content\nwithout,proper")
            temp_path = f.name
        
        try:
            # Pandas handles malformed CSV by creating DataFrame with NaN for missing values
            df = load_project_data(temp_path)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1  # One row with missing data
            assert df.isna().any().any()  # Contains NaN values
        finally:
            os.unlink(temp_path)
    
    def test_load_project_data_empty_file(self):
        """Test loading empty CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("")
            temp_path = f.name
        
        try:
            with pytest.raises(pd.errors.EmptyDataError):
                load_project_data(temp_path)
        finally:
            os.unlink(temp_path)


class TestSplitDataframe:
    """Tests for split_dataframe function."""
    
    def test_split_dataframe_even_length(self, sample_dataframe):
        """Test splitting DataFrame with even number of rows."""
        first_half, second_half = split_dataframe(sample_dataframe)
        
        assert len(first_half) == 2
        assert len(second_half) == 2
        assert first_half.iloc[0]['title'] == 'Project 1'
        assert first_half.iloc[1]['title'] == 'Project 2'
        assert second_half.iloc[0]['title'] == 'Project 3'
        assert second_half.iloc[1]['title'] == 'Project 4'
    
    def test_split_dataframe_odd_length(self):
        """Test splitting DataFrame with odd number of rows."""
        data = {
            'title': ['Project 1', 'Project 2', 'Project 3'],
            'description': ['Desc 1', 'Desc 2', 'Desc 3']
        }
        df = pd.DataFrame(data)
        
        first_half, second_half = split_dataframe(df)
        
        assert len(first_half) == 1
        assert len(second_half) == 2
        assert first_half.iloc[0]['title'] == 'Project 1'
        assert second_half.iloc[0]['title'] == 'Project 2'
    
    def test_split_dataframe_single_row(self):
        """Test splitting DataFrame with single row."""
        data = {'title': ['Project 1'], 'description': ['Desc 1']}
        df = pd.DataFrame(data)
        
        first_half, second_half = split_dataframe(df)
        
        assert len(first_half) == 0
        assert len(second_half) == 1
        assert second_half.iloc[0]['title'] == 'Project 1'
    
    def test_split_dataframe_empty(self):
        """Test splitting empty DataFrame."""
        df = pd.DataFrame()
        
        first_half, second_half = split_dataframe(df)
        
        assert len(first_half) == 0
        assert len(second_half) == 0
        assert first_half.empty
        assert second_half.empty
    
    def test_split_dataframe_invalid_input(self):
        """Test splitting with invalid input."""
        # String input gets split by character position, not an error
        result = split_dataframe("not a dataframe")
        assert result == ("not a d", "ataframe")
        
        # None raises TypeError, not AttributeError
        with pytest.raises(TypeError):
            split_dataframe(None)


class TestRenderFunctions:
    """Tests for render functions using mocks."""
    
    @patch('streamlit.columns')
    @patch('streamlit.image')
    @patch('streamlit.title')
    @patch('streamlit.info')
    def test_render_header_section(self, mock_info, mock_title, mock_image, mock_columns):
        """Test header section rendering."""
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        render_header_section()
        
        mock_columns.assert_called_once_with(2)
        mock_image.assert_called_once_with("images/IMG_2797.JPG")
        mock_title.assert_called_once_with("Jeffrey Crum")
        mock_info.assert_called_once()
    
    @patch('streamlit.write')
    def test_render_intro_text(self, mock_write):
        """Test intro text rendering."""
        render_intro_text()
        
        expected_content = "Below you can find some of the apps I've built in Python. Feel free to contact me!"
        mock_write.assert_called_once_with(expected_content)
    
    @patch('streamlit.header')
    @patch('streamlit.write')
    @patch('streamlit.image')
    def test_render_project_item(self, mock_image, mock_write, mock_header):
        """Test project item rendering."""
        mock_row = pd.Series({
            'title': 'Test Project',
            'description': 'Test Description',
            'url': 'https://example.com',
            'image': 'test.png'
        })
        
        render_project_item(mock_row)
        
        mock_header.assert_called_once_with('Test Project')
        assert mock_write.call_count == 2
        mock_write.assert_any_call('Test Description')
        mock_write.assert_any_call('[Source Code: Test Project](https://example.com)')
        mock_image.assert_called_once_with('images/test.png')
    
    @patch('streamlit.columns')
    @patch('main.render_project_item')
    @patch('main.split_dataframe')
    def test_render_projects_section(self, mock_split, mock_render_item, mock_columns):
        """Test projects section rendering."""
        mock_col3, mock_col4 = MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col3, mock_col4]
        
        first_half = pd.DataFrame({'title': ['Project 1', 'Project 2']})
        second_half = pd.DataFrame({'title': ['Project 3', 'Project 4']})
        mock_split.return_value = (first_half, second_half)
        
        sample_df = pd.DataFrame({'title': ['P1', 'P2', 'P3', 'P4']})
        
        render_projects_section(sample_df)
        
        mock_columns.assert_called_once_with(2)
        mock_split.assert_called_once_with(sample_df)
        assert mock_render_item.call_count == 4
    
    @patch('streamlit.set_page_config')
    @patch('main.render_header_section')
    @patch('main.render_intro_text')
    @patch('main.load_project_data')
    @patch('main.render_projects_section')
    def test_main_function(self, mock_render_projects, mock_load_data, 
                          mock_render_intro, mock_render_header, mock_set_config):
        """Test main function execution."""
        mock_df = pd.DataFrame({'title': ['Test']})
        mock_load_data.return_value = mock_df
        
        main()
        
        mock_set_config.assert_called_once_with(layout="wide")
        mock_render_header.assert_called_once()
        mock_render_intro.assert_called_once()
        mock_load_data.assert_called_once()
        mock_render_projects.assert_called_once_with(mock_df)


class TestEdgeCases:
    """Tests for edge cases and error conditions."""
    
    def test_render_project_item_missing_fields(self):
        """Test project item rendering with missing fields."""
        incomplete_row = pd.Series({'title': 'Test Project'})
        
        with pytest.raises(KeyError):
            render_project_item(incomplete_row)
    
    def test_render_project_item_none_values(self):
        """Test project item rendering with None values."""
        row_with_none = pd.Series({
            'title': None,
            'description': None,
            'url': None,
            'image': None
        })
        
        with patch('streamlit.header') as mock_header, \
             patch('streamlit.write') as mock_write, \
             patch('streamlit.image') as mock_image:
            
            render_project_item(row_with_none)
            
            mock_header.assert_called_once_with(None)
            mock_write.assert_any_call(None)
            mock_image.assert_called_once_with('images/None')
    
    @patch('main.load_project_data')
    def test_main_with_load_error(self, mock_load_data):
        """Test main function when data loading fails."""
        mock_load_data.side_effect = FileNotFoundError("CSV file not found")
        
        with pytest.raises(FileNotFoundError):
            main()