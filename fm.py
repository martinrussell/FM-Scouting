import pandas as pd



# Load the data from HTML
def load_data(html_file_path):
    tables = pd.read_html(html_file_path, encoding='utf-8')
    return tables[0]


# Preprocess data
def preprocess_data(df, attribute_columns):
    for col in df.columns:
        if col in attribute_columns:
            # Extract and process the current score from both possible formats
            df[col + '_Current'] = df[col].apply(
                lambda x: float(str(x).split('-')[0]) if '-' in str(x) and str(x).split('-')[0].strip() else (pd.to_numeric(str(x), errors='coerce') if str(x).strip() else pd.NA)

            )

            # Convert to numeric and handle any errors
            df[col + '_Current'] = pd.to_numeric(df[col + '_Current'], errors='coerce')
        else:
            # Fill NA values with 'Not Available' for non-attribute columns
            df[col] = df[col].fillna('Not Available')

    return df





# Calculate scores for each position
def calculate_position_scores(df, position_weights, attribute_columns):
    max_score = sum(weight * 20 for weight in position_weights['CF'].values())  # Assuming max attribute value is 20

    for position in position_weights:
        df[position + '_Score'] = 0.0
        for index, row in df.iterrows():
            raw_score = sum(row.get(attr + '_Current', 0) * weight for attr, weight in position_weights[position].items() if attr in attribute_columns)
            normalized_score = (raw_score / max_score) * 20  # Scale score to be out of 20
            df.at[index, position + '_Score'] = normalized_score
    return df

def calculate_general_current_score(df, weights, attribute_columns):
    df['Current_Score'] = 0.0
    for index, row in df.iterrows():
        score = sum(row.get(attr + '_Current', 0) * weight for attr, weight in weights.items() if attr in attribute_columns)
        df.at[index, 'Current_Score'] = score
    return df


iwd_weight = {
    'Pas': 0.12,  # Passing: Crucial for ball distribution and helping in build-up play.
    'Dri': 0.12,  # Dribbling: Important for carrying the ball and transitioning from defense to attack.
    'Tck': 0.11,  # Tackling: Essential for winning the ball and defensive duties.
    'Sta': 0.11,  # Stamina: Vital for maintaining high work rate throughout the match.
    'Ant': 0.10,  # Anticipation: Key for reading the game and intercepting passes.
    'Pos': 0.10,  # Positioning: Important for being in the right place defensively and in transition.
    'Dec': 0.09,  # Decisions: Crucial for making the right choices in various situations.
    'Wor': 0.08,  # Work Rate: Necessary for contributing effectively in both offensive and defensive phases.
    'Tec': 0.08,  # Technique: Useful for overall skill in handling the ball.
    'Agi': 0.09,  # Agility: Helps in quick changes of direction and evading opponents.
}



wcb_weight = {
    'Mar': 0.12,  # Marking: Essential for neutralizing opposition attackers, especially in wide areas.
    'Tck': 0.12,  # Tackling: Crucial for dispossessing opponents and preventing attacks.
    'Pas': 0.10,  # Passing: Important for building up play from the back and distributing the ball.
    'Pos': 0.10,  # Positioning: Key for maintaining defensive structure and covering wide areas.
    'Pac': 0.10,  # Pace: Necessary for dealing with fast wingers and covering ground.
    'Ant': 0.10,  # Anticipation: Vital for reading the game and reacting to threats.
    'Str': 0.08,  # Strength: Useful for winning physical duels and aerial battles.
    'Sta': 0.08,  # Stamina: Important for sustaining performance over the full match, especially given the dynamism of the role.
    'Dec': 0.08,  # Decisions: Critical for making the right choices in defensive and transitional situations.
    'Aer': 0.06,  # Aerial Reach: Helpful for defending crosses and contributing to aerial play.
}



bpd_weight = {
    'Pas': 0.12,  # Passing: Essential for distributing the ball and contributing to build-up play.
    'Pos': 0.12,  # Positioning: Key for maintaining the defensive line and being in the right place.
    'Mar': 0.11,  # Marking: Important for neutralizing opposition forwards.
    'Tck': 0.11,  # Tackling: Fundamental for dispossessing opponents and preventing goal-scoring opportunities.
    'Ant': 0.10,  # Anticipation: Vital for reading the game and intercepting passes.
    'Vis': 0.10,  # Vision: Crucial for recognizing passing options and initiating plays.
    'Dec': 0.09,  # Decisions: Critical for making the right choices in various situations.
    'Str': 0.08,  # Strength: Useful for physical duels and aerial battles.
    'Cmp': 0.08,  # Composure: Important for staying calm under pressure and retaining possession.
    'Con': 0.09,  # Concentration: Necessary for maintaining focus throughout the match.
}






dm_weight = {
    'Tck': 0.15,  # Tackling: Essential for dispossessing opponents and breaking up plays.
    'Pos': 0.12,  # Positioning: Crucial for intercepting passes and cutting out attacks.
    'Pas': 0.12,  # Passing: Important for distributing the ball effectively after regaining possession.
    'Ant': 0.10,  # Anticipation: Key for reading the game and being in the right place at the right time.
    'Mar': 0.10,  # Marking: Necessary for neutralizing opposition attackers.
    'Sta': 0.10,  # Stamina: Vital for maintaining performance levels throughout the match.
    'Str': 0.10,  # Strength: Useful for winning physical duels and maintaining control.
    'Dec': 0.08,  # Decisions: Important for choosing the right actions in various situations.
    'Wor': 0.07,  # Work Rate: Critical for covering ground and contributing defensively and offensively.
    'Vis': 0.06,  # Vision: Helpful for spotting and executing effective passes.
}




rpm_weight = {
    'Pas': 0.15,  # Passing: Essential for distributing the ball and controlling the game.
    'Vis': 0.12,  # Vision: Crucial for spotting and creating opportunities.
    'Tec': 0.12,  # Technique: Important for precision in ball control and execution.
    'Sta': 0.10,  # Stamina: Necessary for maintaining energy levels throughout the match.
    'Dri': 0.10,  # Dribbling: Useful for evading opponents and creating space.
    'Ant': 0.10,  # Anticipation: Key for reading the game and reacting appropriately.
    'Dec': 0.10,  # Decisions: Vital for making the right choices in various situations.
    'Wor': 0.07,  # Work Rate: Important for contributing to both offensive and defensive phases.
    'Pos': 0.07,  # Positioning: Helps in being in the right place to receive the ball or cut out opposition plays.
    'Tck': 0.07,  # Tackling: Useful for regaining possession and defensive contributions.
}



iw_weight = {
    'Dri': 0.12,  # Dribbling: Critical for beating defenders and creating space.
    'Pac': 0.11,  # Pace: Essential for quick runs and exploiting space.
    'Tec': 0.11,  # Technique: Important for ball control and skillful play.
    'Sho': 0.11,  # Shooting: Vital for scoring goals, especially when cutting inside.
    'Pas': 0.10,  # Passing: Key for linking up with teammates and creating chances.
    'Fla': 0.10,  # Flair: Useful for unpredictable and creative plays.
    'Otb': 0.10,  # Off-The-Ball: Necessary for intelligent movement and positioning.
    'Vis': 0.09,  # Vision: Crucial for spotting passing opportunities.
    'Agi': 0.08,  # Agility: Helps in quick changes of direction and evading opponents.
    'Cmp': 0.08,  # Composure: Important for staying calm in goal-scoring situations.
}



if_weight = {
    'Fin': 0.12,  # Finishing: Crucial for converting scoring opportunities.
    'Dri': 0.12,  # Dribbling: Essential for beating defenders and creating space.
    'Pac': 0.11,  # Pace: Important for quick runs and exploiting space behind the defense.
    'Tec': 0.11,  # Technique: Key for control and skillful play, especially in tight spaces.
    'Otb': 0.10,  # Off-The-Ball: Necessary for intelligent movement and finding space in the box.
    'Fla': 0.10,  # Flair: Useful for unpredictable and creative plays.
    'Ant': 0.09,  # Anticipation: Vital for reading the game and reacting to goal-scoring opportunities.
    'Agi': 0.08,  # Agility: Helps in quick changes of direction, especially when cutting inside.
    'Cmp': 0.08,  # Composure: Important for keeping calm and making effective decisions in front of goal.
    'Vis': 0.09,  # Vision: Crucial for spotting passing opportunities and linking up with teammates.
}




# Define uniform weights for attributes (adjust based on your criteria)
cf_weight = {
    'Fin': 0.15,  # Finishing: Essential for converting scoring opportunities.
    'Pac': 0.10,  # Pace: Important for making runs behind the defense and quick movements.
    'Dri': 0.10,  # Dribbling: Crucial for beating defenders and creating chances.
    'Fir': 0.10,  # First Touch: Vital for controlling the ball effectively in tight spaces.
    'Str': 0.10,  # Strength: Important for holding up the ball and physical battles.
    'Tec': 0.10,  # Technique: Key for overall ball control and skillful play.
    'Ant': 0.10,  # Anticipation: Critical for positioning in the box and reacting to play.
    'OtB': 0.10,  # Off-The-Ball: Essential for intelligent movement and finding space.
    'Cmp': 0.10,  # Composure: Crucial for maintaining calm and poise in scoring situations.
    'Pas': 0.05,  # Passing: Useful for link-up play and assisting teammates.
}



wb_weight = {
    'Sta': 0.5,  # Stamina for up and down movement on the flank.
    'Pas': 0.4,  # Passing for effective crosses and link-up play.
    'Pac': 0.5,  # Pace to recover defensively and support attacks.
    'Dri': 0.4,  # Dribbling to advance the ball and create chances.
    'Tck': 0.4,  # Tackling for defensive contributions.
    'Cro': 0.4,  # Crossing to provide attacking width.
    # ... other relevant attributes
}


cb_weight = {
    'Pos': 0.12,  # Positioning: Essential for maintaining the defensive line and effective coverage.
    'Mar': 0.12,  # Marking: Crucial for sticking close to opponents and neutralizing threats.
    'Tck': 0.12,  # Tackling: Key for winning the ball and stopping attacks.
    'Str': 0.11,  # Strength: Important for physical battles and aerial dominance.
    'Hea': 0.11,  # Heading: Vital for clearing aerial balls and defending set pieces.
    'Ant': 0.10,  # Anticipation: Necessary for reading the game and making interceptions.
    'Jum': 0.08,  # Jumping Reach: Useful for winning aerial duels.
    'Dec': 0.07,  # Decisions: Important for choosing the right actions in various defensive situations.
    'Cmp': 0.07,  # Composure: Helps in staying calm under pressure and making clear decisions.
    'Con': 0.10,  # Concentration: Crucial for maintaining focus throughout the match.
}



gk_weight = {
    'Ref': 0.6,  # Reflexes for shot-stopping.
    'Han': 0.5,  # Handling to securely catch or parry shots.
    'One': 0.4,  # One on Ones to deal with breakaway situations.
    'Kic': 0.5,  # Kicking for distribution accuracy and range.
    'Pos': 0.4,  # Positioning to cover angles and react to threats.
    'Aer': 0.4,  # Aerial Ability to claim or punch crosses.
    'Com': 0.3,  # Command of Area to organize the defense.
    # ... other relevant attributes
}



position_weights = {
    'WCB': wcb_weight,
    'CB': cb_weight,
    'BPD': bpd_weight,
    'IWD': iwd_weight,
    'RPM': rpm_weight,
    'DM': dm_weight,
    'WB': wb_weight,
    'IW': iw_weight,
    'IF': if_weight,
    'CF': cf_weight,
    'GK': gk_weight   # Weights for Goalkeeper
}




# List of attribute columns
attribute_columns = [
    '1v1', 'Acc', 'Aer', 'Agg', 'Agi', 'Ant', 'Bal', 'Bra', 'Cmd', 'Cnt', 
    'Cmp', 'Cro', 'Dec', 'Det', 'Dri', 'Fin', 'Fir', 'Fla', 'Han', 'Hea', 
    'Jum', 'Kic', 'Ldr', 'Lon', 'Mar', 'Otb', 'Pac', 'Pas', 'Pos', 'Ref', 
    'Sta', 'Str', 'Tck', 'Tea', 'Tec', 'Thr', 'TRO', 'Vis', 'Wor', 'Cor'
]

# Main analysis function
def player_recruitment_analysis(html_file_path):
    df = load_data(html_file_path)
    df = preprocess_data(df, attribute_columns)
    df = calculate_position_scores(df, position_weights, attribute_columns)
    df = calculate_general_current_score(df, position_weights, attribute_columns)  # Calculate the general current score

    final_columns = [
        'Name', 'Position', 'Nat', 'Age', 'Club', 
        'Transfer Value', 'Wage', 
         'Personality', 'Media Handling', 
       'Left Foot', 'Right Foot'
    ]
    final_columns += [pos + '_Score' for pos in position_weights]

    final_df = df[final_columns]
    return final_df.sort_values(by='BPD_Score', ascending=False)

# Save analysis results to an HTML file
def save_to_html(df, output_file_path):
    html_start = '''
    <html>
    <head>
        <title>Player Analysis</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.22/css/jquery.dataTables.css">
        <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.22/js/jquery.dataTables.js"></script>
    </head>
    <body>
    '''

    html_end = '''
<script>
$(document).ready( function () {
    // Find the first table and set its ID to 'player_table'
    $('table').first().attr('id', 'player_table');

    // Initialize DataTables on the table with pagination disabled
    // and custom handling for NaN values during sorting
    $('#player_table').DataTable({
        "paging": false,
        "columnDefs": [{
            "targets": "_all",
            "render": function (data, type, row) {
                return data === 'NaN' || data === null ? '' : data;
            }
        }],
        "order": [] // remove default ordering
    });
} );
</script>
</body>
</html>
'''

# ... rest of the save_to_html





    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_start)
        # Ensure the table ID is set correctly for DataTables
        file.write(df.to_html(index=False, classes='display', table_id='player_table', escape=False))
        file.write(html_end)


    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_start)
        file.write(df.to_html(index=False, classes='display', table_id='player_table', escape=False))
        file.write(html_end)


    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_start)
        file.write(df.to_html(index=False, classes='display', escape=False))
        file.write(html_end)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_start)
        file.write(df.to_html(index=False, classes='display', escape=False))
        file.write(html_end)


# Path to your HTML file
html_file_path = 'cf.html'

# Perform the analysis
df_sorted = player_recruitment_analysis(html_file_path)

# Save the sorted DataFrame to an HTML file
save_to_html(df_sorted, 'scouting.html')

print("Analysis saved to analysis.html")

