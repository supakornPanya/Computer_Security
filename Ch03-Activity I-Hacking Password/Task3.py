import matplotlib.pyplot as plt

# --- Configuration ---
# Change this variable to set your desired security threshold in years
threshold_years = 100

# Define the character set size (upper, lower, digits, special characters)
k = 94

# Define the password lengths to test
lengths = [4, 6, 8, 10, 12]

# TODO: Replace these values with your actual R values (hashes per second) from Problem 2
R_md5 = 816327 
R_sha1 = 1054852
R_bcrypt = 5

# Conversion factor from seconds to years
seconds_in_a_year = 365 * 24 * 60 * 60

# Lists to store the calculated time in years
time_md5 = []
time_sha1 = []
time_bcrypt = []

# Calculate cracking time for each length
print("--- Brute-Force Estimation ---")
for n in lengths:
    # Calculate total combinations (k^n)
    combinations = k ** n
    
    # Calculate time in years for each algorithm
    t_md5_years = (combinations / R_md5) / seconds_in_a_year
    t_sha1_years = (combinations / R_sha1) / seconds_in_a_year
    t_bcrypt_years = (combinations / R_bcrypt) / seconds_in_a_year
    
    # Append results to lists for plotting
    time_md5.append(t_md5_years)
    time_sha1.append(t_sha1_years)
    time_bcrypt.append(t_bcrypt_years)

    # Print the results in a readable scientific notation format
    print(f"Length {n}:")
    print(f"  MD5    : {t_md5_years:.2e} years")
    print(f"  SHA-1  : {t_sha1_years:.2e} years")
    print(f"  Bcrypt : {t_bcrypt_years:.2e} years")
    print("-" * 30)

# Plotting the graph
plt.figure(figsize=(10, 6))

# Plot lines for each algorithm
plt.plot(lengths, time_md5, marker='o', label='MD5')
plt.plot(lengths, time_sha1, marker='s', label='SHA-1')
plt.plot(lengths, time_bcrypt, marker='^', label='Bcrypt')

# Add a horizontal line for the dynamic threshold
plt.axhline(y=threshold_years, color='red', linestyle='--', label=f'{threshold_years}-Year Security Threshold')

# Configure axes, title, and scale
plt.yscale('log') # Use logarithmic scale for Y-axis due to exponential growth
plt.xlabel('Password Length (Characters)')
plt.ylabel('Time to Crack (Years)')
plt.title('Brute-Force Attack Time vs Password Length')
plt.xticks(lengths)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()