using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using ProductAPI.Models;
using System;
using System.Collections.Generic;
using System.Data;
using System.Threading.Tasks;

namespace ProductAPI.Data
{
    public class ProductDbContext
    {
        private readonly string _connectionString;

        public ProductDbContext(IConfiguration configuration)
        {
            // First try to get from Azure Functions configuration (local.settings.json in local dev)
            string? connectionString = configuration.GetValue<string>("SqlConnectionString");
            
            // If not found, try to get from standard .NET configuration (appsettings.json)
            if (string.IsNullOrEmpty(connectionString))
            {
                connectionString = configuration.GetConnectionString("SqlConnectionString");
            }
            
            _connectionString = connectionString ?? 
                throw new ArgumentNullException("SqlConnectionString configuration is missing in both configuration sources");
        }

        public async Task<IEnumerable<Product>> GetAllProductsAsync()
        {
            var products = new List<Product>();
            
            using (var connection = new SqlConnection(_connectionString))
            {
                await connection.OpenAsync();
                
                using var command = new SqlCommand("SELECT * FROM Products", connection);
                using var reader = await command.ExecuteReaderAsync();
                
                while (await reader.ReadAsync())
                {
                    products.Add(MapToProduct(reader));
                }
            }
            
            return products;
        }

        public async Task<Product?> GetProductByIdAsync(int id)
        {
            using var connection = new SqlConnection(_connectionString);
            await connection.OpenAsync();
            
            using var command = new SqlCommand("SELECT * FROM Products WHERE id = @Id", connection);
            command.Parameters.Add("@Id", SqlDbType.Int).Value = id;
            
            using var reader = await command.ExecuteReaderAsync();
            
            if (await reader.ReadAsync())
            {
                return MapToProduct(reader);
            }
            
            return null;
        }

        public async Task<int> CreateProductAsync(Product product)
        {
            using var connection = new SqlConnection(_connectionString);
            await connection.OpenAsync();
            
            using var command = new SqlCommand(
                "INSERT INTO Products (name, description, price, stock_quantity, created_date) " +
                "VALUES (@Name, @Description, @Price, @StockQuantity, @CreatedDate); " +
                "SELECT SCOPE_IDENTITY();", connection);
            
            command.Parameters.Add("@Name", SqlDbType.NVarChar, 100).Value = product.Name;
            command.Parameters.Add("@Description", SqlDbType.NVarChar, 500).Value = product.Description ?? (object)DBNull.Value;
            command.Parameters.Add("@Price", SqlDbType.Decimal).Value = product.Price;
            command.Parameters.Add("@StockQuantity", SqlDbType.Int).Value = product.StockQuantity;
            command.Parameters.Add("@CreatedDate", SqlDbType.DateTime2).Value = DateTime.UtcNow;
            
            var result = await command.ExecuteScalarAsync();
            return Convert.ToInt32(result);
        }

        public async Task<bool> UpdateProductAsync(Product product)
        {
            using var connection = new SqlConnection(_connectionString);
            await connection.OpenAsync();
            
            using var command = new SqlCommand(
                "UPDATE Products SET name = @Name, description = @Description, " +
                "price = @Price, stock_quantity = @StockQuantity, modified_date = @ModifiedDate " +
                "WHERE id = @Id", connection);
            
            command.Parameters.Add("@Id", SqlDbType.Int).Value = product.Id;
            command.Parameters.Add("@Name", SqlDbType.NVarChar, 100).Value = product.Name;
            command.Parameters.Add("@Description", SqlDbType.NVarChar, 500).Value = product.Description ?? (object)DBNull.Value;
            command.Parameters.Add("@Price", SqlDbType.Decimal).Value = product.Price;
            command.Parameters.Add("@StockQuantity", SqlDbType.Int).Value = product.StockQuantity;
            command.Parameters.Add("@ModifiedDate", SqlDbType.DateTime2).Value = DateTime.UtcNow;
            
            int rowsAffected = await command.ExecuteNonQueryAsync();
            return rowsAffected > 0;
        }

        public async Task<bool> DeleteProductAsync(int id)
        {
            using var connection = new SqlConnection(_connectionString);
            await connection.OpenAsync();
            
            using var command = new SqlCommand("DELETE FROM Products WHERE id = @Id", connection);
            command.Parameters.Add("@Id", SqlDbType.Int).Value = id;
            
            int rowsAffected = await command.ExecuteNonQueryAsync();
            return rowsAffected > 0;
        }

        private static Product MapToProduct(SqlDataReader reader)
        {
            return new Product
            {
                Id = reader.GetInt32(reader.GetOrdinal("id")),
                Name = reader.GetString(reader.GetOrdinal("name")),
                Description = reader.IsDBNull(reader.GetOrdinal("description")) 
                    ? null 
                    : reader.GetString(reader.GetOrdinal("description")),
                Price = reader.GetDecimal(reader.GetOrdinal("price")),
                StockQuantity = reader.GetInt32(reader.GetOrdinal("stock_quantity")),
                CreatedDate = reader.GetDateTime(reader.GetOrdinal("created_date")),
                ModifiedDate = reader.IsDBNull(reader.GetOrdinal("modified_date")) 
                    ? null 
                    : reader.GetDateTime(reader.GetOrdinal("modified_date"))
            };
        }
    }
} 